from .api import Source
from contextlib import contextmanager
from rfc6266 import parse_headers
import mimetypes, validators, requests, os, csv


class SourceFactory:
    _instance = None

    def __init__(self):
        self._register = dict()

    def _add(self, mime: str, sourceClass) -> None:
        assert mime is not False, "mime cannot be empty to register "
        assert sourceClass is not None, "sourceClass must be provided" #todo chek it is a proper class, and subclassing Source?
        self._register[mime] = sourceClass


    def _find(self, mime:str):
        return self._register[mime]


    @staticmethod
    def instance():
        if SourceFactory._instance is None:
           SourceFactory._instance = SourceFactory()
        return SourceFactory._instance


    @staticmethod
    def register(mime: str, sourceClass) -> None:
        SourceFactory.instance()._add(mime, sourceClass)


    @staticmethod
    def mime_from_url(url: str) -> str:
        # just get the header, no content yet
        response = requests.head(identifier, allow_redirects=True)
        if response.status_code == 200:
            mime = response.info().get_content_type()
            cdhead = response.headers.get('Content-Disposition')
            if mime == 'application/octet-stream' and cdhead is not None:
                cd = parse_headers(cdhead)
                mime = SourceFactory.mime_from_identifier(cd.filename_sanitized())
        return mime



    @staticmethod
    def mime_from_identifier(identifier: str) -> str:
        # TODO - if identifier matches URL --> perform HEAD request, check response for
        #  1- content-type
        #  2- if application/octet-stream --> also check file-name in content-disposition and prefer that as "identifier" or bargain for best matching mime-type?
        return mimetypes.guess_type(identifier)[0]


    @staticmethod
    def make_source(identifier: str) -> Source:
        remote = False
        if validators.url(identifier):
            remote = True
            mime = SourceFactory.mime_from_remote(identifier)
            assert False, "TODO implement some remote Source decorator or just download the stuff? - see https://github.com/vliz-be-opsci/pyldt/issues/8"

        mime = SourceFactory.mime_from_identifier(identifier)
        sourceClass = SourceFactory.instance()._find(mime)

        return sourceClass(identifier)



class CSVFileSource(Source):
    """
    Source producing iterator over data-set coming from CSV on file
    """
    def __init__ (self, csv_file_path):
        #todo assert if file exists and is readable
        self._csv = csv_file_path

    @contextmanager
    def iterator(self):
        with open(self._csv) as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            yield csvreader

    def __repr__(self):
        return "CSVFileSource('%s')" % os.path.abspath(self._csv)


SourceFactory.register("text/csv", CSVFileSource)
