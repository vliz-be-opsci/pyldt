from pysubyt.api import Sink
from uritemplate import URITemplate, variables
import os


def assert_writable(file_path):
    assert not os.path.isfile(file_path), "File to write '%s' alread exists" % file_path
    parent_path = os.path.dirname(os.path.abspath(file_path))
    assert os.access(parent_path, os.W_OK), "Can not write to folder '%s' for creating new files" % parent_path


class SinkFactory:
    @staticmethod
    def make_sink(identifier: str) -> Sink:
        if identifier is None:
            return StdOutSink()
        # else:
        if len(variables(identifier)) == 0:       # identifier is not a pattern
            return SingleFileSink(identifier)
        # else:                                        #identifier is a pattern
        return PatternedFileSink(identifier)


class StdOutSink(Sink):
    def __init__(self):
        pass

    def __repr__(self):
        return "StdOutSink"

    def close(self):
        pass

    def add(self, part: str, item: dict = None):
        print(part)


class SingleFileSink(Sink):
    def __init__(self, file_path):
        assert_writable(file_path)
        self._file_path = file_path
        self._fopen = open(file_path, "x")

    def __repr__(self):
        return "SingleFileSink('%s')" % os.path.abspath(self._file_path)

    def close(self):
        self._fopen.close()
        self._fopen = None

    def add(self, part: str, item: dict = None):
        assert self._fopen is not None, "File to Sink to already close()d"
        self._fopen.write(part)


class PatternedFileSink(Sink):
    def __init__(self, name_pattern):
        self._name_template = URITemplate(name_pattern)

    def __repr__(self):
        return "PatternedFileSink('%s')" % self._name_template.uri

    def close(self):
        pass

    def add(self, part: str, item: dict = None):
        assert item is not None, "No data context available to expand template"
        file_path = self._name_template.expand(item)
        assert_writable(file_path)
        fopen = open(file_path, "x")
        fopen.write(part)
        fopen.close()
