"""
interpreters - basic

BASIC interpreter
"""

import click
from interpreters.basic.classes import Statement

program = []
program_counter = 0

variables = {}

echo_output = False

def run(file, verbose=False):
    """
    Run the BASIC interpreter on the given file.
    Args:
        file (str): The path to the BASIC file to run.
        verbose (bool): If True, enable verbose output.
    """
    global program, program_counter, echo_output

    if verbose:
        echo_output = True

    # Open the file and read its contents
    with open(file, 'r') as f:
        code = f.read()

    # Split the code into lines
    lines = code.split('\n')

    # Process each line of code into statements
    for line in lines:
        if len(line) == 0:
            continue # Ignore empty lines

        # Convert the code to a list of Statements
        line_num = line.split(maxsplit=1)[0]
        line_stmt = line.split(maxsplit=1)[1]

        try:
            line_num = int(line_num)
        except ValueError:
            click.echo(f"Invalid line number: {line_num}; {line}", err=True)
            exit(1)

        statement = Statement(line_num, line_stmt)

        program.append(statement)

    if len(program) == 0:
        click.echo("No code to run", err=True)
        exit(1)

    program_index = 0
    program_counter = program[program_index].line_number
    max_line = program[-1].line_number

    while program_counter <= max_line:
        # Find the current statement
        for i, statement in enumerate(program):
            if statement.line_number == program_counter:
                program_index = i
                break

        # Parse the statement
        line = program[program_index].statement
        parse(line, program_counter)

        # Increment the program counter
        if program_counter != program[program_index].line_number:
            # GOTO modified this
            continue
        if program_index + 1 >= len(program):
            break # End of program
        program_counter = program[program_index + 1].line_number
        
def parse(line, linenum):
    global program_counter, variables, echo_output
    tokens = line.split()

    if echo_output:
        click.echo(f"Line: {linenum} {line}")

    if len(tokens) == 0:
        return # Ignore empty lines

    if tokens[0] == "PRINT": # PRINT <string>
        # TODO: variable checking
        output = ' '.join(tokens[1:])
        if output.startswith('"') and output.endswith('"'): # TODO: go through each token and have a better error message
            click.echo(output[1:-1], nl=False)
        else:
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

    elif tokens[0] == "PRINTLN":
        output = ' '.join(tokens[1:])
        if output.startswith('"') and output.endswith('"'):
            click.echo(output[1:-1])
        else:
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

    elif tokens[0] == "GOTO": # GOTO <line number>
        if len(tokens) > 2:
            click.echo(f"Unexpected token: {tokens[2]}; {linenum} {line}", err=True)
            exit(1)

        try:
            goto_line = int(tokens[1])
        except ValueError:
            click.echo(f"Invalid line number: {tokens[1]}; {linenum} {line}", err=True)
            exit(1)

        program_counter = goto_line

    elif tokens[0] == "LET": # LET <variable> = <expression>
        if len(tokens) < 4 or tokens[2] != "=":
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

        variable = tokens[1]
        expression = int(tokens[3]) if tokens[3].isdigit() else tokens[3]

        variables[variable] = expression
        if echo_output:
            click.echo(f"LET {variable} = {expression}")

    elif tokens[0] == "REM": # REM <comment>
        return # Ignore comments
    elif tokens[0] == "END": # END
        click.echo("Program ended")
        exit(0)

    elif tokens[0] == "IF": # IF <condition> GOTO <line number>
        if len(tokens) < 6 or tokens[4] != "GOTO":
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

        condition = tokens[1:4]
        goto_line = tokens[5]

        # Evaluate condition (condition: <variable> <operator> <value/variable>)
        if variables.get(condition[0]) is None:
            click.echo(f"Undefined variable: {condition[0]}; {linenum} {line}", err=True)
            exit(1)

        if condition[2].isdigit():
            condition[2] = int(condition[2])
        else:
            if variables.get(condition[2]) is None:
                click.echo(f"Undefined variable: {condition[2]}; {linenum} {line}", err=True)
                exit(1)
            condition[2] = variables[condition[2]]

        condition_valid = False
        if condition[1] == "==":
            condition_valid = variables[condition[0]] == condition[2]
        elif condition[1] == "<":
            condition_valid = variables[condition[0]] < condition[2]
        elif condition[1] == ">":
            condition_valid = variables[condition[0]] > condition[2]
        elif condition[1] == "<=":
            condition_valid = variables[condition[0]] <= condition[2]
        elif condition[1] == ">=":
            condition_valid = variables[condition[0]] >= condition[2]
        elif condition[1] == "!=":
            condition_valid = variables[condition[0]] != condition[2]
        else:
            click.echo(f"Invalid operator: {condition[1]}; {linenum} {line}", err=True)
            exit(1)

        if echo_output:
            click.echo(f"Condition valid: {condition_valid}")

        if condition_valid:
            try:
                goto_line = int(goto_line)
            except ValueError:
                click.echo(f"Invalid line number: {goto_line}; {linenum} {line}", err=True)
                exit(1)

            program_counter = goto_line
        else:
            # Skip the GOTO statement
            pass
 
    elif tokens[0] == "INPUT": # INPUT <variable>
        if len(tokens) != 2:
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

        variable = tokens[1]
        user_input = 0

        valid = False
        while not valid:
            # Get user input
            user_input = click.prompt("")
            try:
                user_input = int(user_input)
            except ValueError:
                click.echo("Input must be an integer")
                continue
            valid = True

        # Store the input in the variables dictionary
        variables[variable] = user_input

    elif tokens[0] == "ELSE":
        if len(tokens) < 3:
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

        if tokens[1] == "GOTO":
            try:
                goto_line = int(tokens[2])
            except ValueError:
                click.echo(f"Invalid line number: {tokens[2]}; {linenum} {line}", err=True)
                exit(1)
            program_counter = goto_line
        elif tokens[1] == "IF":
            if len(tokens) != 7:
                click.echo(f"Syntax error: {linenum} {line}", err=True)
                exit(1)

            condition = tokens[2:4]
            goto_line = tokens[6]
            # Evaluate condition (condition: <variable> <operator> <value/variable>)
            if variables.get(condition[0]) is None:
                click.echo(f"Undefined variable: {condition[0]}; {linenum} {line}", err=True)
                exit(1)
            if condition[2].isdigit():
                condition[2] = int(condition[2])
            else:
                if variables.get(condition[2]) is None:
                    click.echo(f"Undefined variable: {condition[2]}; {linenum} {line}", err=True)
                    exit(1)
                condition[2] = variables[condition[2]]
            condition_valid = False
            if condition[1] == "==":
                condition_valid = variables[condition[0]] == condition[2]
            elif condition[1] == "<":
                condition_valid = variables[condition[0]] < condition[2]
            elif condition[1] == ">":
                condition_valid = variables[condition[0]] > condition[2]
            elif condition[1] == "<=":
                condition_valid = variables[condition[0]] <= condition[2]
            elif condition[1] == ">=":
                condition_valid = variables[condition[0]] >= condition[2]
            elif condition[1] == "!=":
                condition_valid = variables[condition[0]] != condition[2]
            else:
                click.echo(f"Invalid operator: {condition[1]}; {linenum} {line}", err=True)
                exit(1)

            if condition_valid:
                try:
                    goto_line = int(goto_line)
                except ValueError:
                    click.echo(f"Invalid line number: {goto_line}; {linenum} {line}", err=True)
                    exit(1)

                program_counter = goto_line
            else:
                # Skip the GOTO statement
                pass

        else:
            click.echo(f"Syntax error: {linenum} {line}", err=True)
            exit(1)

        # TODO: for, while loops

    else:
        click.echo(f"Unknown command: {tokens[0]}; {linenum} {line}", err=True)
        exit(1)
