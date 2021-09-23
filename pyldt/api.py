from abc import ABC, abstractmethod
from contextlib import contextmanager
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
    def add(self, part: str):
        """
        writes out the part to the sink
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
    def __init__(self, modifiers: str = None):
        self._flatten = True
        self._lowercase = True
        self.load_from_modifiers(modifiers)

    def load_from_modifiers(self, modifiers):
        if modifiers is None:
            return
        # else
        # todo interprete the list of possible modifiers

    def as_modifier_str():
        return "todo"

    def __repr(self):
        return "Settings('%s')" % self._as_modifier_str()

    @staticmethod
    def describe():
        return """
            Todo - a descriptive string of all available modifiers / flags
        """

    @property
    def flatten(self) -> bool:
        return self._flatten

    def lowercase(self) -> bool:
        return self._lowercase


class Generator(ABC):
    """
    Abstract Interface for the actual generation Service
    """
    @abstractmethod
    def process(
        self, template_name: str, inputs: dict, settings: Settings,
        sink: Sink
    ) -> None:
        """
        Process the records found in the _ (base) input and write them to
        the sink

        :param templatename: name of the template to use
        :type template_name: str
        :param input: dict of named Source objects providing content
        :type inputs: dict
        :param settings: Settings object holding the
        """
