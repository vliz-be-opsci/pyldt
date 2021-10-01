from pysubyt import SourceFactory, JinjaBasedGenerator, Settings
import unittest
import os
import string


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


def get_indicator_from_name(name: str, splitter: str = '_', fallback: str = None):
    stem = os.path.splitext(name)[0]
    indicator = stem[stem.index(splitter) + 1:] if splitter in stem else fallback
    return indicator


class TestJinjaGenerator(unittest.TestCase):

    def test_templates(self):
        base = os.path.abspath(os.path.dirname(__file__))
        tpl_path = os.path.join(base, 'templates')
        out_path = os.path.join(base, 'out')
        inp_path = os.path.join(base, 'in')

        g = JinjaBasedGenerator(tpl_path)

        inputs = dict()
        inp_names = next(os.walk(inp_path), (None, None, []))[2]  # [] if no file
        for inp_name in inp_names:
            key = get_indicator_from_name(inp_name, fallback='_')
            inputs[key] = SourceFactory.make_source(os.path.join(inp_path, inp_name))

        sink = AssertingSink(self)

        # read all names (files) in the tpl_path
        names = next(os.walk(tpl_path), (None, None, []))[2]  # [] if no file

        for name in names:
            # load the expected parts from the matching output-file in the sink
            sink.load_parts(get_expected_parts(os.path.join(out_path, name)))
            settings = Settings(get_indicator_from_name(name))

            # process
            g.process(name, inputs, settings, sink)

            # assure all records were passed
            sink.close()


if __name__ == '__main__':
    unittest.main()
