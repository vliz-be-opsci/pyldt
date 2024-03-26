import os
import time
import unittest
from pathlib import Path

import pandas as pd

from pysubyt import Subyt


class TestConditional(unittest.TestCase):
    """
    Test case based on examples/subyt_conditional.py
    """

    def test_conditional(self):
        if Path("./tests/tmp/data/A.ttl").exists():
            os.remove("./tests/tmp/data/A.ttl")

        if Path("./tests/tmp/data/D.ttl").exists():
            os.remove("./tests/tmp/data/D.ttl")

        # first run
        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime1 = os.stat("./tests/tmp/data/A.ttl").st_mtime

        # second run and no updates to input file
        time.sleep(1)
        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime2 = os.stat("./tests/tmp/data/A.ttl").st_mtime
        assert A_mtime1 == A_mtime2  # output file should not have been updated

        # third run and update to input file
        time.sleep(1)
        df = pd.read_csv("./tests/resources/data.csv")
        df.at[0, "value"] = 0
        df.to_csv("./tests/resources/data.csv", index=False)
        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime3 = os.stat("./tests/tmp/data/A.ttl").st_mtime
        assert A_mtime1 < A_mtime3  # output file should have been updated

        # fourth run and no updates to input file
        time.sleep(1)
        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime4 = os.stat("./tests/tmp/data/A.ttl").st_mtime
        D_mtime4 = os.stat("./tests/tmp/data/D.ttl").st_mtime
        assert A_mtime3 == A_mtime4  # output file should not have been updated

        # fifth run and one of the output files is missing
        time.sleep(1)
        os.remove("./tests/tmp/data/D.ttl")
        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime5 = os.stat("./tests/tmp/data/A.ttl").st_mtime
        D_mtime5 = os.stat("./tests/tmp/data/D.ttl").st_mtime
        assert A_mtime4 == A_mtime5  # output file should not have been updated
        assert D_mtime4 < D_mtime5  # output file should have been updated

        # reset input file
        df = pd.read_csv("./tests/resources/data.csv")
        df.at[0, "value"] = 1
        df.to_csv("./tests/resources/data.csv", index=False)
