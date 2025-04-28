"""
interpreters - basic

BASIC interpreter
"""

import click
import interpreters.basic.classes as classes

environment = {}

program = []

parse_line_number = 0

def run(file, verbose=False):
    """
    Run the BASIC interpreter on the given file.
    Args:
        file (str): The path to the BASIC file to run.
        verbose (bool): If True, enable verbose output.
    """
    global environment

    if verbose:
        environment['__verbose'] = True

    # Open the file and read its contents
    with open(file, 'r') as f:
        code = f.read()


    # PARSING STEP

    # Split the code into lines
    lines = code.split('\n')
    for line in lines:
        if len(line) == 0:
            continue
        # Parse the line into a Line object
        line_obj = parse_line(line)

        if verbose:
            click.echo(f"Parsed: {line} -> {line_obj}")

        program.append(line_obj)



def parse_line(line):
    """
    Parse a line of BASIC code.
    Args:
        line (str): A line of BASIC code.
    Returns:
        Line: A Line object representing the parsed line.
    """
    global parse_line_number

    line_parts = line.split(" ", 1) # Separate line number and actual code
    if len(line_parts) == 1: # No line number (so sequential line number instead)
        line_number = parse_line_number
        parse_line_number += 1
        code = line_parts[0]
    else:
        line_number = int(line_parts[0])
        code = line_parts[1]

    # Tokenize the code
    tokens = tokenize(code)
    return line(line_number, parse_tokens(tokens))

def tokenize(line):
    """
    Tokenize a line of BASIC code.
    Args:
        line (str): A line of BASIC code.
    Returns:
        list: A list of tokens.
    """
    tokens = []
    token = ""
    in_string = False
    in_comment = False

    for char in line:
        if char == '"':
            in_string = not in_string
            token += char
        elif char.isspace() and not in_string and not in_comment:
            if token:
                tokens.append(token.strip())
                token = ""
        else:
            token += char

    if token:
        tokens.append(token.strip())

    return tokens

def parse_tokens(tokens):
    """
    Parse a list of tokens into a BASIC expression.
    Args:
        tokens (list): A list of tokens.
    Returns:
        Expression: The parsed expression.
    """

    if len(tokens) == 0:
        return None

    keyword = tokens.pop(0).upper()

    if keyword == "LET":
        return parse_let_stmt(tokens)
    elif keyword == "PRINT":
        return parse_print_stmt(tokens)
    elif keyword == "INPUT":
        return parse_input_stmt(tokens)
    elif keyword == "GOTO":
        return parse_goto_stmt(tokens)

def parse_expression(tokens):
    """
    Parse a list of tokens into a BASIC expression.
    Args:
        tokens (list): A list of tokens.
    Returns:
        Expression: The parsed expression.
    """
    
    # EXPRESSION: VALUE [ OPERATOR EXPRESSION ] | '(' EXPRESSION ')'

    if len(tokens) == 0:
        return None

    # Case: '(' EXPRESSION ')'
    if tokens[0] == "(":
        # Handle parentheses
        tokens.pop(0)
        expr = parse_expression(tokens[:-1])
        if tokens and tokens[0] == ")":
            tokens.pop(0)
            return expr
        else:
            raise ValueError("Mismatched parentheses")

    # Case: VALUE
    if len(tokens) == 1:
        token = tokens.pop(0)
        if token.isdigit():
            return classes.Value(int(token))
        else:
            return classes.Identifier(token)
 
    # Case: VALUE [ OPERATOR EXPRESSION ]

    if len(tokens) > 1:
        token = tokens.pop(0)
        if token.isdigit():
            left = classes.Value(int(token))
        else:
            left = classes.Identifier(token)

        if len(tokens) > 1:
            operator = tokens.pop(0)
            right = parse_expression(tokens)
            return classes.Expression(left, operator, right)

# LET <variable> = <expression>
def parse_let_stmt(tokens):
    """
    Parse a LET statement.
    Args:
        tokens (list): A list of tokens.
    Returns:
        LetStatement: The parsed LET statement.
    """

    line = ' '.join(tokens)

    if len(tokens) < 3 or tokens[1] != "=":
        raise ValueError("Invalid LET statement")

    identifier = classes.Identifier(tokens[0])
    expression = parse_expression(tokens[2:])

    return classes.LetStatement(line, identifier, expression)

def parse_print_stmt(tokens):
    pass

def parse_input_stmt(tokens):
    pass

def parse_goto_stmt(tokens):
    pass

def parse_if_stmt(tokens):
    pass

