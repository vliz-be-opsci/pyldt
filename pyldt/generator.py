# Use this file to describe the datamodel handled by this module
# we recommend using abstract classes to achieve proper service and interface insulation

from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader, meta
import os
from .functions import Functions
from .api import Generator, Settings, Sink, Source, log

class JinjaBasedGenerator(Generator):
    """
    Core class for the jinja based LD Templating service.
    """

    def __init__(self, templates_folder: str ):
        """
        Builds the generator that produces LD uplifted variants from datasources

        :param templates_folder: Location of the templates
        """
        if templates_folder is None:
            templates_folder = "."
        self._templates_folder = templates_folder
        self._templates_env = Environment(loader=FileSystemLoader(self._templates_folder))

    def __repr__ (self):
        return "JinjaBasedGenerator('%s')" % os.path.abspath(self._templates_folder)

    def process(self, template_name: str, inputs: dict,  settings: Settings, sink: Sink) -> None:
        ldt = self._templates_env.get_template(template_name)
        base = inputs.pop('_', None)

        # TODO check for " collection " modifier --> or missing _ base source --> then do not iterate but run once !
        # TODO insert also a ctrl object with control info that the template creator can use:
        #   -- isFirst: boolean, isLast: boolean, modus="row|collection", index: sequence-number of the row
        assert base is not None
        with base.iterator() as data:
            for item in data:
                # todo check " flattening " modifier --> when flattening is needed the item should be flattened
                # similar processing could be handled through the settings object itself?
                record = item
                log.debug("processing record _ = %s" % record)
                part = ldt.render(_=record, sets=input, fn=Functions.all())
                sink.add(part)
