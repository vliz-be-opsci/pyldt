import os
import time
import unittest
from pathlib import Path

from util4tests import log, run_single_test

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

        data_mtime0 = os.stat("./tests/resources/data.csv").st_mtime

        # first run
        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime1 = os.stat("./tests/tmp/data/A.ttl").st_mtime
        log.debug(f"A.ttl exists and lastmod at {A_mtime1}")

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
        assert A_mtime1 == A_mtime2, "A.ttl output should not been updated"
        log.debug(f"A.ttl lastmod still at {A_mtime2}")

        # third run and update to input file
        Path("./tests/resources/data.csv").touch()
        data_mtime3 = os.stat("./tests/resources/data.csv").st_mtime
        log.debug(f"data.csv updated at {data_mtime3}")
        assert data_mtime0 < data_mtime3, "data file not updated"
        assert A_mtime1 < data_mtime3, "data still older then last output"
        time.sleep(1)

        Subyt(
            source="./tests/resources/data.csv",
            sink="./tests/tmp/data/{key}.ttl",
            template_name="data.ttl.j2",
            template_folder="./tests/resources",
            conditional=True,
        ).process()
        A_mtime3 = os.stat("./tests/tmp/data/A.ttl").st_mtime
        assert A_mtime1 < A_mtime3, "A.ttl output should been updated"
        assert data_mtime3 < A_mtime3, (
            "A.ttl output file should be newer then data input"
            f"{data_mtime3} < {A_mtime3}"
        )

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
        assert A_mtime3 == A_mtime4, "A.ttl output should not been updated"

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
        assert A_mtime4 == A_mtime5, "A.ttl output should not been updated"
        assert D_mtime4 < D_mtime5, "D.ttl output should been updated"


if __name__ == "__main__":
    run_single_test(__file__)
