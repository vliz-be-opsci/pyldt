from .api import Sink


class StdOutSink(Sink) :
    def __init__ (self):
       pass

    def add(self, part: str):
        print(part)

    def __repr__(self):
        return "StdOutSink"


class SinkFactory:
    @staticmethod
    def make_sink(identifier: str) -> Sink:
        if identifier is None:
            return StdOutSink()
        # else
        assert False, "Todo provide implementation for FileSink -- see https://github.com/vliz-be-opsci/pyldt/issues/7"
