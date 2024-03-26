"""
Example of running pysubyt as a python library.
This examples uses the no-it mode to generate a single data.ttl from a data.csv
file.
Run this script from the root of the repository.
"""

import logging

from pysubyt import Subyt

logging.basicConfig(level=logging.INFO)

subyt = Subyt(
    extra_sources={"data": "./tests/resources/data.csv"},
    sink="./examples/data/data.ttl",
    template_name="data_no-it.ttl.j2",
    template_folder="./tests/resources",
    mode="no-it",
)

subyt.process()
