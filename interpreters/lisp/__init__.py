"""
interpreters/lisp

LISP interpreter
"""

import click

from interpreters.lisp.classes import LispExpression, LispAtom, LispSymbol, LispList

environment = {
    "true": True,
    "false": False,
    "nil": None,
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
}

def run(file, verbose=False):
    """
    Run the LISP interpreter on the given file.
    Args:
        file (str): The path to the LISP file to run.
        verbose (bool): If True, enable verbose output.
    """
    global environment

    if verbose:
        environment["__interpreter_verbose"] = True

    # Open the file and read its contents
    with open(file, 'r') as f:
        code = f.read()

    # Split the code into lines
    lines = code.split('\n')

    # Process each line of code into expressions
    for line in lines:
        if len(line) == 0:
            continue  # Ignore empty lines

        # Convert the code to a list of expressions
        expression = parse_expression(line)

        print(expression)

        # Evaluate the expression
        result = expression.evaluate(environment)

        if verbose:
            click.echo(f"Evaluated: {line} -> {result}")

def parse_expression(line):
    """
    Parse a line of code into a LISP expression.
    Args:
        line (str): The line of code to parse.
    Returns:
        LispExpression: The parsed LISP expression.
    """
    tokens = tokenize(line)
    return parse_tokens(tokens)

def tokenize(line):
    """
    Tokenize a line of code into LISP tokens.
    Args:
        line (str): The line of code to tokenize.
    Returns:
        list: A list of tokens.
    """
    tokens = []
    token = ""
    in_string = False

    for char in line:
        if char == "(":
            if token:
                tokens.append(token)
                token = ""
            tokens.append("(")
            print(tokens)
            continue

        if char == ")":
            if token:
                tokens.append(token)
                token = ""
            tokens.append(")")
            print(tokens)
            continue

        if char == '"':
            in_string = not in_string
            if not in_string:
                tokens.append(token)
                token = ""

            print(tokens)
            continue

        if char.isspace() and not in_string:
            if token:
                tokens.append(token)
                token = ""
            print(tokens)
            continue

        token += char

    if token:
        tokens.append(token)

    print(tokens)

    return tokens

def parse_tokens(tokens):
    """
    Parse a list of tokens into a LISP expression.
    Args:
        tokens (list): The list of tokens to parse.
    Returns:
        LispExpression: The parsed LISP expression.
    """
    if len(tokens) == 0:
        return None

    token = tokens.pop(0)


    if token == "(":
        elements = []
        while tokens[0] != ")":
            elements.append(parse_tokens(tokens))
        tokens.pop(0)  # Remove the closing parenthesis
        return LispList(elements)
    elif token == ")":
        raise ValueError("Unexpected closing parenthesis")
    else:
        if token.isdigit():
            return LispAtom(int(token))
        return LispSymbol(token)
