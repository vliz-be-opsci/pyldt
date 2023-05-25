# -*- coding: utf-8 -*-
import argparse
import logging
import logging.config
import sys

from pysubyt.api import Generator, Settings, Sink
from pysubyt.j2.generator import JinjaBasedGenerator
from pysubyt.sinks import SinkFactory
from pysubyt.sources import SourceFactory

log = logging.getLogger(__name__)


def get_arg_parser():
    """
    Defines the arguments to this script by using Python's
    [argparse](https://docs.python.org/3/library/argparse.html)
    """
    parser = argparse.ArgumentParser(
        description="Produces LD triples a Template",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-l",
        "--logconf",
        type=str,
        action="store",
        help="location of the logging config (yml) to use",
    )

    parser.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="Speficies the name of the template to use",
    )

    parser.add_argument(
        "-s",
        "--set",
        nargs=2,  # each -s should have 2 arguments
        metavar=("KEY", "FILE"),  # meaning/purpose of those arguments
        action="append",  # multiple -s can be combined
        help=(
            "Multiple entries will add different sets "
            'under sets["KEY"] to the templating process'
        ),
    )

    parser.add_argument(
        "-v",
        "--var",
        nargs=2,  # each -v should have 2 arguments
        metavar=("NAME", "VALUE"),  # meaning/purpose of those arguments
        action="append",  # multiple -v can be combined
        help=(
            "Multiple entries will add different named"
            " variables to the templating process"
        ),
    )

    parser.add_argument(
        "-t",
        "--templates",
        metavar="FOLDER",  # meaning of the argument
        action="store",
        default=".",  # local working directory
        help="Passes the context folder holding all the templates",
    )
    parser.add_argument(
        "-i",
        "--input",
        metavar="FILE",  # meaning of the argument
        action="store",
        help=(
            "Specifies the base input set to run over."
            " Shorthand for -s _ FILE"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE|PATTERN",  # meaning of the argument
        action="store",
        help="Specifies where to write the output, can use {uritemplate}.",
    )
    parser.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help=(
            "Force writing output, do not check "
            "if output files already exist."
        ),
    )
    parser.add_argument(
        "-m",
        "--mode",
        metavar=" (no-)it(eration), (no-)ig(norecase), (no-)fl(atten) ",
        action="store",
        help="""Modifies the mode of iteration:
                1. it (default) vs. no-it: apply template for each
                                                iterated row in the input set
                                           vs. apply it only once once for
                                                the complete input set;
                2. ig vs. no-ig: to be implemented;
                3. fl vs. no-fl: to be implemented.""",
    )
    return parser


def make_service(args: argparse.Namespace) -> Generator:
    template_folder = args.templates
    return JinjaBasedGenerator(template_folder)


def make_sources(args: argparse.Namespace) -> dict:
    inputs = dict()
    if args.input is not None:
        inputs["_"] = SourceFactory.make_source(args.input)
    if args.set is not None:
        for [key, file_name] in args.set:
            inputs[key] = SourceFactory.make_source(file_name)
    return inputs


def make_sink(args: argparse.Namespace) -> Sink:
    return SinkFactory.make_sink(args.output, args.force)


def vars_to_dict(vars: list) -> dict:
    if not vars:
        return None
    # else
    return {name: value for [name, value] in vars}


def enable_logging(args: argparse.Namespace):
    if args.logconf is None:
        return
    import yaml  # conditional dependency -- we only need this (for now)

    # when logconf needs to be read

    with open(args.logconf, "r") as yml_logconf:
        logging.config.dictConfig(
            yaml.load(yml_logconf, Loader=yaml.SafeLoader)
        )
    log.info(f"Logging enabled according to config in {args.logconf}")


def main():
    """
    The main entry point to this module.
    """
    args = get_arg_parser().parse_args()

    enable_logging(args)
    service = make_service(args)
    settings = Settings(args.mode)
    vars_dict = vars_to_dict(args.var)
    inputs = make_sources(args)
    sink = make_sink(args)

    try:
        log.debug("service  = %s" % service)
        log.debug("settings = %s" % settings)
        log.debug("variables = %s" % vars_dict)
        log.debug("inputs   = %s" % inputs)
        log.debug("sink     = %s" % sink)

        service.process(args.name, inputs, settings, sink, vars_dict)

        log.debug("processing done")

    except Exception as e:
        errmsg = "pysubyt processing failed due to <%s>" % e
        log.error(errmsg)
        log.exception(e)
        print("*** ERROR *** " + errmsg, file=sys.stderr)

    finally:
        sink.close()


if __name__ == "__main__":
    main()
