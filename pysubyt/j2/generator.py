import os
from typing import Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pyrdfj2 import Filters, Functions

from pysubyt.api import Generator


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
            loader=FileSystemLoader(self._templates_folder),
            autoescape=select_autoescape(
                disabled_extensions=("ttl", "txt", "ldt", "json", "jsonld"),
                default_for_string=True,
                default=True,
            ),
        )
        self._templates_env.globals = Functions.all()
        # Since  the change ttl -> xsd, and removal of ttl to filters
        # But this seems a bit redundact.
        self._templates_env.globals.update(Filters.all())
        self._templates_env.filters.update(Filters.all())

    def __repr__(self):
        abs_folder = os.path.abspath(self._templates_folder)
        return "JinjaBasedGenerator('%s')" % abs_folder

    def make_render_fn(self, template_name: str) -> Callable:
        return self._templates_env.get_template(template_name).render
