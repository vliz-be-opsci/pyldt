"""
Example of running pysubyt on a conditional basis.
Only when the input data has been updated, a new output file is generated.
Run this script from the root of the repository.
"""

import logging

from pysubyt import Subyt

logging.basicConfig(level=logging.INFO)

subyt_it = Subyt(
    source="./tests/resources/data.csv",
    sink="./examples/data/{key}.ttl",
    template_name="data.ttl.j2",
    template_folder="./tests/resources",
    conditional=True,
)

subyt_it.process()

subyt_no_it = Subyt(
    extra_sources={"data": "./tests/resources/data.csv"},
    sink="./examples/data/data.ttl",
    template_name="data_no-it.ttl.j2",
    template_folder="./tests/resources",
    mode="no-it",
    conditional=True,
)

subyt_no_it.process()
