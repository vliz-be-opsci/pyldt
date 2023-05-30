import glob
import logging
import mimetypes
import os
import re
from typing import Callable

import requests
import validators
from typeguard import check_type

from pysubyt.api import Source

log = logging.getLogger(__name__)


def assert_readable(file_path):
    assert os.path.isfile(file_path), (
        "File to read '%s' does not exists" % file_path
    )
    assert os.access(file_path, os.R_OK), "Can not read '%s'" % file_path


def fname_from_cdisp(cdisp):
    return re.split(r"; ?filename=", cdisp, flags=re.IGNORECASE)


class SourceFactory:
    _instance = None

    def __init__(self):
        self._register = dict()
        self._ext_mime_map = {"csv": "text/csv"}

    @property
    def ext_2_mime(self):
        return self._ext_mime_map

    def _add(self, mime: str, sourceClass: Callable[[str], Source]) -> None:
        assert mime is not False, "mime cannot be empty to register "
        assert sourceClass is not None, "sourceClass must be provided"
        check_type(sourceClass, Callable[[str], Source])

        self._register[mime] = sourceClass

    def _find(self, mime: str):
        assert mime in self._register, (
            "no Source class available for mime '%s'" % mime
        )
        return self._register[mime]

    @staticmethod
    def instance():
        if SourceFactory._instance is None:
            SourceFactory._instance = SourceFactory()
        return SourceFactory._instance

    @staticmethod
    def register(mime: str, sourceClass: Callable[[str], Source]) -> None:
        SourceFactory.instance()._add(mime, sourceClass)

    @staticmethod
    def map(ext: str, mime: str) -> None:
        SourceFactory.instance().ext_2_mime[ext] = mime

    @staticmethod
    def mime_from_url(url: str) -> str:
        # just get the header, no content yet
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            mime: str = response.info().get_content_type()
            cdhead = response.headers.get("Content-Disposition")
            if mime == "application/octet-stream" and cdhead is not None:
                cd = fname_from_cdisp(cdhead)
                mime = SourceFactory.mime_from_identifier(cd)
        return mime

    @staticmethod
    def mime_from_identifier(identifier: str) -> str:
        ext = identifier.split(".")[-1]
        mime = SourceFactory.instance().ext_2_mime.get(ext)
        log.debug(f"mapping ext '{ext}' to mime '{mime}'")
        if mime is not None:
            return mime
        # else
        return mimetypes.guess_type(identifier)[0]

    @staticmethod
    def make_source(identifier: str) -> Source:
        if validators.url(identifier):
            mime: str = SourceFactory.mime_from_remote(identifier)
            assert False, "TODO remote Source support - see issues #8"

        # else
        if os.path.isdir(identifier):
            source = FolderSource(identifier)
            return source

        # else
        if glob.has_magic(identifier):
            source = GlobSource(identifier)
            return source

        # else
        mime: str = SourceFactory.mime_from_identifier(identifier)
        assert mime is not None, (
            "no valid mime derived from identifier '%s'" % identifier
        )
        sourceClass: Callable[[str], Source] = SourceFactory.instance()._find(
            mime
        )
        source: Source = sourceClass(identifier)

        return source


class FolderSource(Source):
    def __init__(self, folder_path):
        self._folder = os.path.abspath(folder_path)
        self._sourcefiles = sorted(
            list(next(os.walk(self._folder), (None, None, []))[2])
        )
        assert len(self._sourcefiles) > 0, (
            "FolderSource '%s' should have content files." % self._folder
        )
        self._reset()

    def __repr__(self):
        return "%s('%s')" % (type(self), self._folder)

    def _reset(self):
        self._current_source = None
        self._current_iter = None
        self._ix = -1

    def _exitCurrent(self):
        if self._current_source is not None:
            self._current_source.__exit__()

    def _nextSource(self):
        self._exitCurrent()
        self._ix += 1
        if self._ix < len(self._sourcefiles):
            self._current_source = SourceFactory.make_source(
                os.path.join(self._folder, self._sourcefiles[self._ix])
            )
            self._current_iter = self._current_source.__enter__()
        else:
            self._current_source = None
            self._current_iter = None
            raise StopIteration

    def _nextItem(self):
        # proceed to next element, if needed, proceed to next source
        if self._current_source is None:
            self._nextSource()
        try:
            return next(self._current_iter)
        except StopIteration:
            self._nextSource()
            return next(self._current_iter)
        # else
        raise StopIteration

    def __enter__(self):
        class IterProxy:
            def __init__(self, me):
                self._me = me

            def __iter__(self):
                self._me._reset()
                return self

            def __next__(self):
                return self._me._nextItem()

        return IterProxy(self)

    def __exit__(self):
        # exit the current open source
        self._exitCurrent()
        self._reset()


class GlobSource(FolderSource):
    """For now, this class is inheriting from FolderSource. As soon as another
    class appears with similar behavior to FolderSource and GlobSource, we may
    consider to create an abstract class "CollectionSource" and make all of
    theminherit from this abstract class.
    """

    def __init__(self, pattern, pattern_root_dir="."):
        self._folder = pattern_root_dir
        self._sourcefiles = sorted(
            [p for p in glob.glob(pattern) if os.path.isfile(p)]
        )
        assert len(self._sourcefiles) > 0, (
            "GlobSource '%s' should have content files." % self._folder
        )
        self._reset()


try:
    import csv

    class CSVFileSource(Source):
        """
        Source producing iterator over data-set coming from CSV on file
        """

        def __init__(self, csv_file_path):
            assert_readable(csv_file_path)
            self._csv = csv_file_path

        def __enter__(self):
            self._csvfile = open(self._csv, mode="r", encoding="utf-8-sig")
            return csv.DictReader(self._csvfile, delimiter=",")

        def __exit__(self):
            self._csvfile.close()

        def __repr__(self):
            return "CSVFileSource('%s')" % os.path.abspath(self._csv)

    SourceFactory.register("text/csv", CSVFileSource)
    # wrong, yet useful mime for csv:
    SourceFactory.register("application/csv", CSVFileSource)
except ImportError:
    log.warn("Python CSV module not available -- disabling CSV support!")


try:
    import json

    class JsonFileSource(Source):
        """
        Source producing iterator over data-set coming from json on file
        """

        def __init__(self, json_file_path):
            assert_readable(json_file_path)
            self._json = json_file_path

        def __enter__(self):
            # note this is loading everything in memory
            #   -- will not work for large sets
            #   in the future we might need to consider:
            #   (json-stream)[https://pypi.org/project/json-stream/]
            with open(self._json, mode="r", encoding="utf-8-sig") as jsonfile:
                data = json.load(jsonfile)
                # unwrap nested structures
                while isinstance(data, dict) and len(data.keys()) == 1:
                    child = list(data.values())[0]
                    if isinstance(child, dict) and len(child.keys()) == 0:
                        data = [data]
                    else:
                        data = child
                if not isinstance(data, list):
                    data = [data]
            return iter(data)

        def __exit__(self):
            pass

        def __repr__(self):
            return "JsonFileSource('%s')" % os.path.abspath(self._json)

    SourceFactory.register("application/json", JsonFileSource)
except ImportError:
    log.warn("Python JSON module not available -- disabling JSON support!")


try:
    import xmlasdict

    class XMLFileSource(Source):
        """
        Source producing iterator over data-set coming from XML on file
        """

        def __init__(self, xml_file_path):
            assert_readable(xml_file_path)
            self._xml = xml_file_path

        def __enter__(self):
            with open(self._xml, mode="r", encoding="utf-8-sig") as xmlfile:
                xml_str = xmlfile.read()
                xdict = xmlasdict.parse(xml_str)
                # unpack root wrappers
                data = xdict.unpack()

            return iter(data)

        def __exit__(self):
            pass

        def __repr__(self):
            return "XMLFileSource('%s')" % os.path.abspath(self._xml)

    SourceFactory.map("eml", "text/xml")
    SourceFactory.register("text/xml", XMLFileSource)
    # wrong, yet useful mime for xml:
    SourceFactory.register("application/xml", XMLFileSource)
except ImportError:
    log.warn("Python XML module not available -- disabling XML support!")
