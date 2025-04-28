"""
interpreters.py

Entry point for the interpreters module.
"""

import click

from interpreters.basic import run as run_basic
from interpreters.lisp import run as run_lisp

@click.group()
def interpreters():
    pass

@interpreters.command()
@click.option("--file", "-f", "filename", required=False, type=click.Path(exists=True), help="Path to the BASIC file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def basic(filename, verbose):
    # TODO: implement a basic interpreter througn command line
    run_basic(filename, verbose=verbose)

@interpreters.command()
@click.argument("filename")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def lisp(filename, verbose):
    run_lisp(filename, verbose=verbose)

interpreters.add_command(basic, "basic")
interpreters.add_command(lisp, "lisp")

if __name__ == "__main__":
    interpreters()
