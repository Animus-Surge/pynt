"""
interpreters.py

Entry point for the interpreters module.
"""

import click

from interpreters.basic import run as run_basic
from interpreters.lisp import run as run_lisp
from interpreters.lc3 import run as run_lc3

from interpreters.basic.repl import repl as run_basic_repl

@click.group()
def interpreters():
    pass

@interpreters.command()
@click.option("--file", "-f", "filename", required=False, type=click.Path(exists=True), help="Path to the BASIC file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def basic(filename, verbose):
    # TODO: implement a basic interpreter througn command line
    if filename is None:
        run_basic_repl(verbose=verbose)
    else:
        run_basic(filename, verbose=verbose)

@interpreters.command()
@click.argument("filename")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def lisp(filename, verbose):
    run_lisp(filename, verbose=verbose)

@interpreters.command()
@click.argument("filename")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def lc3(filename, verbose):
    run_lc3(filename, verbose=verbose)

interpreters.add_command(basic, "basic")
interpreters.add_command(lisp, "lisp")
interpreters.add_command(lc3, "lc3")

if __name__ == "__main__":
    interpreters()
