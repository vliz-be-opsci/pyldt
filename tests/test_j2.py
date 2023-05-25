import os

from pysubyt.j2.generator import JinjaBasedGenerator


def test_JinjaBasedGenerator():
    jb_generator = JinjaBasedGenerator(None)
    abs_folder = os.path.abspath(".")
    assert jb_generator._templates_folder == "."
    assert str(jb_generator) == "JinjaBasedGenerator('%s')" % abs_folder
