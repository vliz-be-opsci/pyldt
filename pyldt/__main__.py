# -*- coding: utf-8 -*-
import argparse
import sys
from .generator import Generator, JinjaBasedGenerator
from .api import Sink, Settings, log
from .sources import SourceFactory
from .sinks import SinkFactory


def get_arg_parser():
    """
    Defines the arguments to this script by using Python's
    [argparse](https://docs.python.org/3/library/argparse.html)
    """
    parser = argparse.ArgumentParser(
        description='Produces LD triples a Template',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-n', '--name',
        action='store',
        required=True,
        help='Speficies the name of the template to use'
    )

    parser.add_argument(
        '-s', '--set',
        nargs=2,                      # each -s should have 2 arguments
        metavar=('KEY', 'FILE'),      # meaning/purpose of those arguments
        action="append",              # multiple -s can be combined
        help='Multiple entries will add different sets under sets["KEY"] to the templating process',
    )

    parser.add_argument(
        '-t', '--templates',
        metavar="FOLDER",             # meaning of the argument
        action="store",
        default='.',                  # local working directory
        help='Passes the context folder holding all the templates',
    )
    parser.add_argument(
        '-i', '--input',
        metavar="FILE",               # meaning of the argument
        action="store",
        help='Specifies the base input set to run over. Shorthand for -s _ FILE',
    )
    parser.add_argument(
        '-o', '--output',
        metavar="FILE|PATTERN",       # meaning of the argument
        action="store",
        help='Specifies where to write the output, can use {uritemplate}.',
    )
    parser.add_argument(
        '-f', '--flags',
        metavar=" (no-)ig(norecase),(no-)fl(atten),(no-)it(eration) ",
        action="store",
        help='Modifies the mode of operation through some flags',
    )
    return parser


def make_service(args: argparse.Namespace) -> Generator:
    template_folder = args.templates
    return JinjaBasedGenerator(template_folder)


def make_sources(args: argparse.Namespace) -> dict:
    inputs = dict()
    if args.input is not None:
        inputs['_'] = SourceFactory.make_source(args.input)
    if args.set is not None:
        for [key, file_name] in args.set:
            inputs[key] = SourceFactory.make_source(file_name)
    return inputs


def make_sink(args: argparse.Namespace) -> Sink:
    return SinkFactory.make_sink(args.output)


def main():
    """
    The main entry point to this module.
    """
    args = get_arg_parser().parse_args()

    service = make_service(args)
    settings = Settings(args.flags)
    inputs = make_sources(args)
    sink = make_sink(args)

    try:
        log.debug("service  = %s" % service)
        log.debug("settings = %s" % settings)
        log.debug("inputs   = %s" % inputs)
        log.debug("sink     = %s" % sink)

        service.process(args.name, inputs, settings, sink)

        log.debug("processing done")

    except Exception as e:
        errmsg = "pyldt processing failed due to <%s>" % e
        log.error(errmsg)
        print("*** ERROR *** " + errmsg, file=sys.stderr)

    finally:
        sink.close()


if __name__ == '__main__':
    main()
