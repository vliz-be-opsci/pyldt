from jinja2 import Environment, FileSystemLoader
from .functions import Functions
from .api import Generator, Settings, Sink, log
import os


class JinjaBasedGenerator(Generator):
    """
    Core class for the jinja based LD Templating service.
    """

    def __init__(self, templates_folder: str):
        """
        Builds the generator that produces LD output from datasources

        :param templates_folder: Location of the templates
        """
        if templates_folder is None:
            templates_folder = "."
        self._templates_folder = templates_folder
        self._templates_env = Environment(
            loader=FileSystemLoader(self._templates_folder))

    def __repr__(self):
        abs_folder = os.path.abspath(self._templates_folder)
        return "JinjaBasedGenerator('%s')" % abs_folder

    def process(
        self, template_name: str, inputs: dict, settings: Settings, sink: Sink
    ) -> None:
        ldt = self._templates_env.get_template(template_name)
        base = inputs.pop('_', None)

        # TODO check for " collection " modifier --> or missing _ base source
        #  --> then do not iterate but run once !
        # TODO insert also a ctrl object with control info
        #  --> see pyldt/issues/2
        assert base is not None
        with base.iterator() as data:
            for item in data:
                # TODO check " flattening " modifier
                #  --> see pyldt/issues/4
                record = item
                log.debug("processing record _ = %s" % record)
                part = ldt.render(_=record, sets=input, fn=Functions.all())
                sink.add(part)
