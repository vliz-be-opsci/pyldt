"""
Example of running pysubyt as a python library.
This examples uses the "it" mode to generate a multiple {key}.ttl files from a
single data.csv file.
Run this script from the root of the repository.
"""

import logging

from pysubyt import Subyt

logging.basicConfig(level=logging.INFO)

subyt = Subyt(
    source="./tests/resources/data.csv",
    sink="./examples/data/{key}.ttl",
    template_name="data.ttl.j2",
    template_folder="./tests/resources",
)

subyt.process()
