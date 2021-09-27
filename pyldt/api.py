from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Dict
import logging


logname = 'pyldt'
logfile = logname + '.log'
logging.basicConfig(level=logging.DEBUG, filename=logfile)
log = logging.getLogger(logname)


class Sink(ABC):
    """
    Abstract Interface for sinks
    """

    @abstractmethod
    def close(self):
        """
        notifies the Sink all writing has been done - allows cleanup
        """

    @abstractmethod
    def add(self, part: str, item: dict = None):
        """
        writes out the part to the sink

        :param part: the result for a sepcific part that needs to be sinked
        :type part: str
        :param item: the record for which this part was produced
        :type item: dict
        """


class Source(ABC):
    """
    Abstract Interface for input Sources
    """

    @abstractmethod
    @contextmanager
    def iterator(self):
        return []


class Settings:
    """
    Embodies all the actual possible modifiers to the process
    """

    _scheme: Dict[str, Dict] = {
        "ignorecase":  {
            "default": True,
            "description": "Make all keys lowercase so to ignore case in key references"
        },
        "flatten":  {
            "default": True,
            "description": "Flatten hierarchical strcutures by making hierarchical key references."
        },
        "iteration": {
            "default": True,
            "description": "Perform the iteration outside of the template to avoid looping inside of it"
        },
    }
    _negation: str = "no-"

    def __init__(self, modifiers: str = None):
        self._values = {key: val['default'] for (key, val) in Settings._scheme.items()}
        self.load_from_modifiers(modifiers)

    def load_from_modifiers(self, modifiers: str):
        """
        Parses the -m --mode string into actual properties
        (no-)ig(norecase),(no-)fl(atten),(no-)it(eration)
        """
        if modifiers is None:
            return
        # else
        set_parts: Dict[str, bool] = {key: False for (key, val) in self._values.items()}

        for part in modifiers.split(','):
            val: bool = True
            if part.startswith(Settings._negation):
                val = False
                part = part[len(Settings._negation):]
            found = [key for (key, val) in self._values.items() if key.startswith(part)]
            assert len(found) == 1, "ambiguous modifier string '%s' matches list: %s" % (part, found)
            key = found[0]
            assert not set_parts[key], "ambiguous modifier string '%s' matches key '%s' which is already set" % (part, key)
            set_parts[key] = True
            self._values[key] = val

    def as_modifier_str(self) -> str:
        """
        Reproduces the modifier string that declares these settings
        """
        return ','.join(['no-' + key if not val else key for (key, val) in self._values.items()])

    def __repr__(self) -> str:
        return "Settings('%s')" % self.as_modifier_str()

    @staticmethod
    def describe() -> str:
        return '\n'.join(["%30s: %s" % (key, val['description']) for (key, val) in Settings._scheme.items()])

    def __getattr__(self, key) -> bool:
        return self._values[key]


class Generator(ABC):
    """
    Abstract Interface for the actual generation Service
    """
    @abstractmethod
    def process(
        self, template_name: str, inputs: Dict[str, Source], settings: Settings,
        sink: Sink
    ) -> None:
        """
        Process the records found in the base input and write them to the sink.
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
