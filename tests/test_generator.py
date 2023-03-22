from pysubyt import SourceFactory, Sink, JinjaBasedGenerator, Settings
import unittest
import os
from util4tests import run_single_test, log


class AssertingSink(Sink):
    def __init__(self, test):
        self._test = test
        self._parts = []

    def load_parts(self, parts):
        self._parts = parts
        self._index = 0

    def _assert_count(self):
        self._test.assertEqual(self._index, len(self._parts))

    def add(self, part: str, item: dict = None):
        log.debug("part received no. %d:\n--\n%s\n--" % (self._index, part))
        expected = self._parts[self._index].strip()
        part = part.strip()
        log.debug(f"expected part == \n{expected}\n")
        log.debug(f"actual part == \n{part}\n")
        log.debug(f"expectations ok: {bool(part == expected)}")
        self._test.assertEqual(
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
    known_cases = {"data_glob/*.json": "glob"}
    if name in known_cases.keys():
        return known_cases[name]
    stem = os.path.splitext(name)[0]
    indicator = stem[stem.index(splitter) + 1:] if splitter in stem else fallback
    return indicator


class TestJinjaGenerator(unittest.TestCase):

    def test_templates(self):
        log.debug("beginning test_templates")
        self.maxDiff = None
        base = os.path.abspath(os.path.dirname(__file__))
        tpl_path = os.path.join(base, 'templates')
        out_path = os.path.join(base, 'out')
        inp_path = os.path.join(base, 'in')

        g = JinjaBasedGenerator(tpl_path)

        inputs = dict()
        inp_content = next(os.walk(inp_path), (None, None, []))  # the stuff in the folder
        inp_names = list(inp_content[2])   # the files
        inp_names.extend(inp_content[1])   # the folders too
        inp_names = [i for i in inp_names if i != "data_glob"]  # filter "data_glob" folder source out
        inp_names.extend(["data_glob/*.json"])  # insert "glob pattern" glob source
        for inp_name in inp_names:
            key = get_indicator_from_name(inp_name, fallback='_')
            assert key not in inputs, "duplicate key '%s' for input '%s' --> object[%s]" % (key, inp_name, inputs[key])
            inputs[key] = SourceFactory.make_source(os.path.join(inp_path, inp_name))

        self.assertTrue('_' in inputs, 'the base set should be available')
        sink = AssertingSink(self)

        # read all names (files) in the tpl_path
        names = next(os.walk(tpl_path), (None, None, []))[2]  # [] if no file

        for name in names:
            # load the expected parts from the matching output-file in the sink
            sink.load_parts(get_expected_parts(os.path.join(out_path, name)))
            settings = Settings(get_indicator_from_name(name))

            # process
            log.debug("processing test-template: %s " % os.path.join(tpl_path, name))
            g.process(name, inputs, settings, sink, vars_dict={"my_domain": "realexample.org"})

            # assure all records were passed
            sink.close()
        log.debug("ending test_templates")


if __name__ == '__main__':
    run_single_test(__file__)
