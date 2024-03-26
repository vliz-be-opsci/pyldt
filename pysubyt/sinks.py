import logging
import os
from pathlib import Path

from uritemplate import URITemplate, variables

from pysubyt.api import Sink

logger = logging.getLogger(__name__)


def assert_writable(file_path: str, force_output: bool = False):
    if not force_output:
        assert not os.path.isfile(file_path), (
            "File to write '%s' alread exists" % file_path
        )
    parent_path = os.path.dirname(os.path.abspath(file_path))
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    assert os.access(parent_path, os.W_OK), (
        "Can not write to folder '%s' for creating new files" % parent_path
    )


class SinkFactory:
    @staticmethod
    def make_sink(
        identifier: str,
        force_output: bool = False,
        allow_repeated_sink_paths: bool = False,
    ) -> Sink:
        if identifier is None:
            if allow_repeated_sink_paths:
                logger.warning(
                    "repeated sink paths do not apply to StdOutSink, "
                    "ignoring..."
                )
            return StdOutSink()
        # else:
        if len(variables(identifier)) == 0:  # identifier is not a pattern
            if allow_repeated_sink_paths:
                logger.warning(
                    "repeated sink paths do not apply to SingleFileSink, "
                    "ignoring..."
                )
            return SingleFileSink(identifier, force_output)
        # else:                                        #identifier is a pattern
        return PatternedFileSink(
            identifier, force_output, allow_repeated_sink_paths
        )


class StdOutSink(Sink):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "StdOutSink"

    def open(self):
        pass

    def close(self):
        pass

    def add(self, part: str, item: dict = None, source_mtime: float = None):
        print(part)


class SingleFileSink(Sink):
    def __init__(self, file_path: str, force_output: bool = False):
        super().__init__()
        assert_writable(file_path, force_output)
        self._file_path = file_path
        self._force_output = force_output
        if Path(file_path).exists():
            self.mtimes = {file_path: os.stat(file_path).st_mtime}

    def __repr__(self):
        return "SingleFileSink('%s', %s)" % (
            os.path.abspath(self._file_path),
            self._force_output,
        )

    def open(self):
        self._fopen = open(self._file_path, "w")

    def close(self):
        self._fopen.close()
        self._fopen = None

    def add(self, part: str, item: dict = None, source_mtime: float = None):
        assert self._fopen is not None, "File to Sink to already closed"
        logger.info(f"Creating {self._file_path}")
        self._fopen.write(part)


class PatternedFileSink(Sink):
    def __init__(
        self,
        name_pattern: str,
        force_output: bool = False,
        allow_repeated_sink_paths: bool = False,
    ):
        super().__init__()
        self._name_template = URITemplate(name_pattern)
        self._force_output = force_output
        self._allow_repeated_sink_paths = allow_repeated_sink_paths
        self._file_paths = []
        self.mtimes = None

    def __repr__(self):
        return "PatternedFileSink('%s', %s)" % (
            self._name_template.uri,
            self._force_output,
        )

    def open(self):
        pass

    def close(self):
        pass

    def _add(self, file_path: str, part: str, source_mtime: float = None):
        sink_mtime = (
            os.stat(file_path).st_mtime if Path(file_path).exists() else 0
        )
        if source_mtime and (source_mtime < sink_mtime):
            logger.info(
                f"Aborting creation of {file_path} "
                f"(source_mtime = {source_mtime}; sink_mtime = {sink_mtime})"
            )
            return
        assert_writable(file_path, self._force_output)
        logger.info(f"Creating {file_path}")
        with open(file_path, "w") as f:
            f.write(part)

    def add(self, part: str, item: dict = None, source_mtime: float = None):
        assert item is not None, "No data context available to expand template"
        file_path = self._name_template.expand(item)
        if self._allow_repeated_sink_paths:
            extended_file_path = file_path[:]
            if file_path in self._file_paths:
                extended_file_path = (
                    f"{file_path}_{self._file_paths.count(file_path) - 1}"
                )
            self._add(extended_file_path, part, source_mtime)
        else:
            if file_path in self._file_paths:
                raise RuntimeError(
                    f"{file_path} was already created in this process, "
                    "make sure data items are not duplicated or "
                    "set allow_repeated_sink_paths to True"
                )
            self._add(file_path, part, source_mtime)
        self._file_paths.append(file_path)
