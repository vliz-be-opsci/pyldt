from .api import Source
from contextlib import contextmanager
from rfc6266 import parse_headers, ContentDisposition
from typing import Callable
from typeguard import check_type
import mimetypes
import validators
import requests
import os
import csv


def assert_readable(file_path):
    assert os.path.isfile(file_path), "File to read '%s' does not exists" % file_path
    assert os.access(file_path, os.R_OK), "Can not read '%s'" % file_path


class SourceFactory:
    _instance = None

    def __init__(self):
        self._register = dict()

    def _add(self, mime: str, sourceClass: Callable[[str], Source]) -> None:
        assert mime is not False, "mime cannot be empty to register "
        assert sourceClass is not None, "sourceClass must be provided"
        check_type('Source <Constructor>', sourceClass, Callable[[str], Source])

        self._register[mime] = sourceClass

    def _find(self, mime: str):
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
    def mime_from_url(url: str) -> str:
        # just get the header, no content yet
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            mime: str = response.info().get_content_type()
            cdhead: ContentDisposition = response.headers.get('Content-Disposition')
            if mime == 'application/octet-stream' and cdhead is not None:
                cd = parse_headers(cdhead)
                mime = SourceFactory.mime_from_identifier(
                    cd.filename_sanitized())
        return mime

    @staticmethod
    def mime_from_identifier(identifier: str) -> str:
        return mimetypes.guess_type(identifier)[0]

    @staticmethod
    def make_source(identifier: str) -> Source:
        if validators.url(identifier):
            mime: str = SourceFactory.mime_from_remote(identifier)
            assert False, "TODO remote Source support - see issues #8"

        mime: str = SourceFactory.mime_from_identifier(identifier)
        sourceClass: Callable[[str], Source] = SourceFactory.instance()._find(mime)
        source: Source = sourceClass(identifier)

        return source


class CSVFileSource(Source):
    """
    Source producing iterator over data-set coming from CSV on file
    """
    def __init__(self, csv_file_path):
        assert_readable(csv_file_path)
        self._csv = csv_file_path

    @contextmanager
    def iterator(self):
        with open(self._csv, mode="r", encoding="utf-8-sig") as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            yield csvreader

    def __repr__(self):
        return "CSVFileSource('%s')" % os.path.abspath(self._csv)


SourceFactory.register("text/csv", CSVFileSource)
