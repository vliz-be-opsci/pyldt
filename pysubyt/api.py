import itertools
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Callable, Dict

log = logging.getLogger(__name__)


class Sink(ABC):
    """Abstract Interface for sinks"""

    @abstractmethod
    def close(self):
        """Notifies the Sink all writing has been done - allows cleanup"""

    @abstractmethod
    def add(self, part: str, item: dict = None):
        """Writes out the part to the sink

        :param part: the result for a sepcific part that needs to be sinked
        :type part: str
        :param item: the record for which this part was produced
        :type item: dict
        """


class Source(ABC):
    """Abstract Interface for input Sources - mainly context-manager
    for the actual Iterable to be returned"""

    @abstractmethod
    def __enter__(self) -> Iterable:
        """Source context is expected to yield an Iterable"""

    @abstractmethod
    def __exit__(self, *exc):
        """Source context cleanup"""


# TODO make a pandas source in sources.py


class Settings:
    """Embodies all the actual possible modifiers to the process"""

    _scheme: Dict[str, Dict] = {
        "ignorecase": {
            "default": True,
            "description": (
                "Make all keys lowercase so "
                "to ignore case in key references"
            ),
        },
        "flatten": {
            "default": True,
            "description": (
                "Flatten hierarchical strcutures"
                " by making hierarchical key references."
            ),
        },
        "iteration": {
            "default": True,
            "description": (
                "Perform the iteration outside of "
                "the template to avoid looping inside of it"
            ),
        },
    }
    _negation: str = "no-"

    @staticmethod
    def describe() -> str:
        return "\n".join(
            [
                "%30s: %s" % (key, val["description"])
                for (key, val) in Settings._scheme.items()
            ]
        )

    def __init__(self, modifiers: str = None):
        self._values = {
            key: val["default"] for (key, val) in Settings._scheme.items()
        }
        self.load_from_modifiers(modifiers)

    def load_from_modifiers(self, modifiers: str):
        """
        Parses the -m --mode string into actual properties
        (no-)ig(norecase),(no-)fl(atten),(no-)it(eration)
        """
        if modifiers is None:
            return
        # else
        set_parts: Dict[str, bool] = {
            key: False for (key, val) in self._values.items()
        }

        for part in modifiers.split(","):
            val: bool = True
            if part.startswith(Settings._negation):
                val = False
                part = part[len(Settings._negation) :]
            found = [
                key
                for (key, val) in self._values.items()
                if key.startswith(part)
            ]
            assert (
                len(found) == 1
            ), "ambiguous modifier string '%s' matches list: %s" % (
                part,
                found,
            )
            key = found[0]
            assert not set_parts[key], (
                "ambiguous modifier string "
                f"{part} matches key {key} which is already set"
            )
            set_parts[key] = True
            self._values[key] = val

    def as_modifier_str(self) -> str:
        """
        Reproduces the modifier string that declares these settings
        """
        return ",".join(
            [
                "no-" + key if not val else key
                for (key, val) in self._values.items()
            ]
        )

    def __repr__(self) -> str:
        return "Settings('%s')" % self.as_modifier_str()

    def __getattr__(self, key: str) -> bool:
        return self._values[key]

    def __setattr__(self, key: str, val: bool) -> None:
        if key in ["_values"]:  # actual props to be handled through super
            super(Settings, self).__setattr__(key, val)
            return
        # else  --> dynamic props to be stored in self._values
        if key not in Settings._scheme.keys():
            raise KeyError(
                "attribute '%s' not writeable in Settings object" % key
            )
        self._values[key] = val


class ReIterableAccess(dict):
    """Helper class wraps around an existing dict of iterables,
    making it posible to access the members so that they return
    independent object wrappers that insure totally
    independent iterating loops into them
    """

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __getitem__(self, key: str) -> Iterable:
        it = dict.__getitem__(self, key)
        # itertools.tee, makes retrieved iterators iterable again
        #   after accessing it from this dict again
        it, cln = itertools.tee(it, 2)
        dict.__setitem__(self, key, it)
        return cln

    def __setitem__(self, key: str, val: Iterable):
        assert isinstance(
            val, Iterable
        ), "This dict only accepts Iterable objects as value"
        dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return "%s(%s)" % (type(self).__name__, dictrepr)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class IteratorsFromSources(dict):
    """
    Helper class managing the context entry of the various sources.
    """

    def __enter__(self):
        iterators = dict()
        for name, source in self.items():
            it = source.__enter__()
            iterators[name] = it
        return ReIterableAccess(iterators)

    def __exit__(self, *exc):
        for name, source in self.items():
            source.__exit__()


class Generator(ABC):
    """Abstract Base Class for the actual generation Service"""

    @abstractmethod
    def make_render_fn(self, template_name: str) -> Callable:
        """Produces the actual render strategy tied to a specific
        templating implementation"""

    def make_processor(
        self,
        template_name: str,
        sets: Dict[str, Iterable],
        settings: Settings,
        sink: Sink,
        vars_dict: dict = None,
    ):
        return Generator.Processor(
            self.make_render_fn(template_name), sets, settings, sink, vars_dict
        )

    class Processor:
        """Rendition proces Manager - controls queue, manages context

        This mainly introduces
          (1) a fifo queue of one item allowing to detect and mark the 'last'
            element of an iteration
          (2) abstracts the actual template rendition to a Callable function
            producing text out of context ``**kvargs``
        """

        def __init__(
            self,
            render_fn: Callable,
            sets: Dict[str, Iterable],
            settings: Settings,
            sink: Sink,
            vars_dict: dict = None,
        ):
            self.render = render_fn
            self.sets = sets
            self.settings = settings
            self.sink = sink
            self.variables = vars_dict if vars_dict is not None else {}
            self.queued_item = None
            self.isFirst = True
            self.isLast = False
            self.index = 0

        def take(self, next_item):
            """Takes next item to be rendered and synced
                (might queue up to next take before actually processing)

            Pushes the previous taken item out,
                and puts the new item in the queue
            """
            assert (
                next_item is not None
            ), "no item to take - use all_taken() for finalization in stead"
            if not self.isFirst or (
                self.isFirst and self.queued_item is not None
            ):  # on first call only queue
                self.push()
            self.queued_item = next_item

        def all_taken(self):
            """Indicates all items have been taken -- finalization

            Will push the last item (already queued)
            """
            self.isLast = True
            self.push()

        def push(self):
            """Actually pushes the item queued"""
            item = self.queued_item
            log.debug("processing item _ = %s" % item)
            part = self.render(
                _=item,
                sets=self.sets,
                ctrl={
                    "isFirst": self.isFirst,
                    "isLast": self.isLast,
                    "index": self.index,
                    "settings": self.settings,
                },
                **self.variables,
            )
            self.sink.add(part, item)
            self.queued_item = None
            self.isFirst = False
            self.index += 1

    def process(
        self,
        template_name: str,
        inputs: Dict[str, Source],
        settings: Settings,
        sink: Sink,
        vars_dict: dict = None,
    ) -> None:
        """Process the records found in the base input and
            write them to the sink.
        Note the base input is expected to be found at inputs['_']

        :param template_name: name of the template to use
        :type template_name: str
        :param input: dict of named Source objects providing content
        :type inputs: Dict[str, Source]
        :param settings: Settings object holding the
        :type settings: Settings
        :param sink: the sink to write result to
        :type sink: Sink
        """
        # convert inputs into sets
        with IteratorsFromSources(inputs) as sets:
            proc = self.make_processor(
                template_name, sets, settings, sink, vars_dict
            )

            if (
                not settings.iteration or "_" not in sets
            ):  # conditions for collection modus
                settings.iteration = False
                proc.all_taken()
            else:  # default modus
                data = sets["_"]
                for item in data:
                    proc.take(item)
                proc.all_taken()
