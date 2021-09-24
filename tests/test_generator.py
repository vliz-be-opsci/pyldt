import unittest
import os
import string
from pyldt import SourceFactory, JinjaBasedGenerator, Settings


class AssertingSink:
    def __init__(self, test):
        self._test = test
        self._parts = []

    def load_parts(self, parts):
        self._parts = parts
        self._index = 0

    def _assert_count(self):
        self._test.assertEquals(self._index, len(self._parts))

    def add(self, part: str, item: dict = None):
        table = str.maketrans('', '', string.whitespace)
        expected = self._parts[self._index].translate(table)
        part = part.translate(table)
        self._test.assertEquals(
            expected, part,
            "unexpected rendering for part at index %d" % self._index)
        self._index += 1

    def close(self):
        self._assert_count()


def get_expected_parts(outfile):
    parts = ['']
    n = 0
    with open(outfile, 'r') as content:
        for line in content:
            if not line.startswith('#'):
                parts[n] = parts[n] + line
            else:
                if len(parts[n]) > 0:
                    parts.append('')
                    n += 1
    return parts


class TestJinjaGenerator(unittest.TestCase):

    def test_something(self):
        base = os.path.abspath(os.path.dirname(__file__))
        ldt_path = os.path.join(base, 'ldt')
        out_path = os.path.join(base, 'out')
        print("using templates in ", ldt_path)

        g = JinjaBasedGenerator(ldt_path)

        settings = Settings()

        sets = dict()
        sets["_"] = SourceFactory.make_source(os.path.join(base, "data.csv"))

        sink = AssertingSink(self)

        # read all names (files) in the ldt_path
        names = next(os.walk(ldt_path), (None, None, []))[2]  # [] if no file

        for name in names:
            # load the expected parts from the matching output-file in the sink
            sink.load_parts(get_expected_parts(os.path.join(out_path, name)))

            # process
            g.process(name, sets, settings, sink)

            # assure all records were passed
            sink.close()


if __name__ == '__main__':
    unittest.main()
