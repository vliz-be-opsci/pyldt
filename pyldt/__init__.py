""" pyldt

.. module:: pyldt
    :synopsis: python implementation of LinkedData Templates support
    to produce triples out of various datasources

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""

from .api import Sink, Source, Settings, Generator
from .generator import JinjaBasedGenerator
from .sources import SourceFactory
from .sinks import SinkFactory

__all__ = [
    "Sink", "Source", "Settings", "Generator",
    "JinjaBasedGenerator", "SourceFactory", "SinkFactory"]
