"""
Example of running pysubyt in "it" mode with duplicated data items.
Run this script from the root of the repository.
"""

import logging

from pysubyt import Subyt

logging.basicConfig(level=logging.INFO)

subyt = Subyt(
    source="./tests/resources/data_with_repeated_identifiers.csv",
    sink="./examples/data/{key}.ttl",
    template_name="data.ttl.j2",
    template_folder="./tests/resources",
    conditional=True,
    allow_repeated_sink_paths=True,
)

subyt.process()
