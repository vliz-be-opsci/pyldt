import unittest
from pathlib import Path

from pysubyt import Subyt


class TestRepeatedSinkPaths(unittest.TestCase):
    """
    Test case based on examples/subyt_duplicated_data_items.py
    """

    def test_allow_repeated_sink_paths(self):
        Subyt(
            source="./tests/resources/data_with_repeated_identifiers.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
            allow_repeated_sink_paths=True,
        ).process()
        assert Path("./tests/tmp/data/D.ttl").exists()
        assert Path("./tests/tmp/data/D.ttl_0").exists()
        assert Path("./tests/tmp/data/D.ttl_1").exists()

    def test_disallow_repeated_sink_paths(self):
        subyt = Subyt(
            source="./tests/resources/data_with_repeated_identifiers.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        )
        self.assertRaises(RuntimeError, subyt.process)
