# -*- coding: utf-8 -*-
import argparse
import sys

from .api import *
from .generator import JinjaBasedGenerator



def get_arg_parser():
    """
    Defines the arguments to this script by using Python's [argparse](https://docs.python.org/3/library/argparse.html)

    """
    parser = argparse.ArgumentParser(description='Produces LD triples out of various datasources using a template',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-n', '--name', action='store', required=True, help='Speficies the name of the template to use')

    # TODO make -s
    #   ask for 2 arguments - name and inputfile
    #   be able to be used multiple times --> action = append?
    parser.add_argument('-s', '--sets', help='Adds a set to the process' )

    parser.add_argument('-t', '--templates', help='Passes the context folder holding all the templates', default='.')
    parser.add_argument('-i', '--input', help='Specifies the base input set to run over')
    parser.add_argument('-o', '--output', help='Specifies where to write the output to - van be a {{template}} pattern itself.')
    parser.add_argument('-f', '--flags', help='Modifies the mode of operation through some flags')
    return parser


def make_service(args: argparse.Namespace) -> Generator:
    template_folder = args.templates
    return JinjaBasedGenerator(template_folder)

def make_sources(args: argparse.Namespace) -> dict:
    inputs = dict()
    if args.input is not None:
        inputs['_'] = CSVFileSource(args.input)
    if args.sets is not None:
        assert True == False, "failing --sets  to load additional input sets is not yet supported"
    return inputs

def make_sink(args:argparse.Namespace ) -> Sink:
    if args.output is None:
        return StdOutSink()
    #else
    assert True == False, "failing --output is not yet supported, we just dump results to stdout for now"

def main():
    """
    The main entry point to this module.

    """
    args = get_arg_parser().parse_args()

    service = make_service(args)
    settings = Settings(args.flags)
    inputs = make_sources(args)
    sink = make_sink(args)

    log.debug("service  = %s" % service)
    log.debug("settings = %s" % settings)
    log.debug("inputs   = %s" % inputs)
    log.debug("sink     = %s" % sink)

    service.process(args.name, inputs, settings, sink)
    log.debug("processing done")


if __name__ == '__main__':
    main()
