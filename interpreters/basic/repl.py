"""
interpreters/basic/repl.py
REPL implementation for BASIC interpreter
"""

import click
import signal

from interpreters.basic import *

_old_echo = click.echo
def _safe_echo(*args, **kwargs):
    """
    A safe echo function that handles exceptions.
    """
    try:
        _old_echo(*args, **kwargs)
    except KeyboardInterrupt:
        pass

click.echo = _safe_echo

def sigint(signal, frame):
    global environment
    """
    Signal handler for SIGINT (Ctrl+C).
    """

    try:
        if environment["__running"]:
            click.echo("\nStopping run.")
            environment["__running"] = False
        else:
            click.echo("\nExit.")
            environment["__running"] = False
            exit(0)
    except Exception as e:
        click.echo(f"Exception caught!: {e}")
        environment["__running"] = False

environment = {
    "__program_counter": 0,
    "__max_line_number": 0,
    "__current_line": -1,
    "__verbose": False,
    "__running": False
}

program = {}

def repl(verbose=False):
    """
    Read-Eval-Print Loop (REPL) for BASIC interpreter.
    """
    global environment
    global program

    signal.signal(signal.SIGINT, sigint)

    click.echo("Welcome to the BASIC REPL! Type 'exit' to quit.")
    
    while True:
        try:
            # Read input
            line = click.prompt("BASIC> ", type=str)
            
            # Parse and execute the command
            if line.strip():
                command(line.strip())

        except Exception as e:
            raise e

def command(user_input):
    """
    Execute a command in the REPL.
    """
    global environment
    global program

    if user_input.lower() == "exit":
        click.echo("Exit.")
        exit(0)

    elif user_input.lower() == "list":
        if not program:
            click.echo("No program loaded.")
        else:
            for line_number in sorted(program.keys()):
                click.echo(f"{line_number}: {program[line_number]}")
    elif user_input.lower() == "run":
        environment["__running"] = True
        environment["__program_counter"] = 0
        run_loop()
    elif user_input.lower() == "new":
        program.clear()
        environment["__program_counter"] = 0
        environment["__current_line"] = -1
        environment["__max_line_number"] = 0
        click.echo("New program created.")

    elif user_input.split()[0].isdigit():
        line_number = int(user_input.split()[0])
        line = parse_line(user_input)
        program[line_number] = line

    else:
        click.echo(f"Unknown command: {user_input}")

def run_loop():
    """
    Run the BASIC program in a loop.
    """
    global environment
    global program

    click.echo("Running program...")

    program_line_numbers = list(program.keys())
    environment['__program_counter'] = 0
    environment['__max_line_number'] = max(program_line_numbers)
    environment['__current_line'] = -1

    while environment['__program_counter'] < environment['__max_line_number']:

        # Startup
        if environment['__current_line'] == -1:
            try:
                environment['__current_line'] = program_line_numbers[environment['__program_counter']]
            except IndexError:
                click.echo("No program loaded.")
                break
        else:
            line_index = program_line_numbers.index(environment['__current_line'])
            if line_index != environment['__program_counter']:
                # Means a GOTO has occured
                environment['__program_counter'] = line_index
            else:
                environment['__program_counter'] += 1

        if environment['__program_counter'] >= len(program_line_numbers):
            break
        
        if not environment['__running']: # Ctrl+C
            break

        environment['__current_line'] = program_line_numbers[environment['__program_counter']]

        if environment['__verbose']:
            click.echo(f"Executing line {environment['__current_line']}")

        line = program[environment['__current_line']]
        if environment['__verbose']:
            click.echo(f"Line: {line}")

        # Execute the line
        line.execute(environment)

    environment['__running'] = False
