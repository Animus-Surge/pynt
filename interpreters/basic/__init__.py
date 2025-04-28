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

    # EXECUTION STEP
    # Set program counter
    environment['__program_counter'] = 0
    current_position = environment['__program_counter']
    current_position_index = -1
    max_line_number = max(line.linenum for line in program)

    # Handle potential infinite loops
    loop_counter = 0
    max_loops = 1000
    previous_position = None

    # Execute the program
    while environment["__program_counter"] < max_line_number:
        # Starting position
        if current_position_index == -1:
            current_position = program[0].linenum
            environment["__program_counter"] = current_position
            current_position_index = 0

        # Handle control flow
        elif current_position == environment["__program_counter"]:
            previous_position = current_position
            current_position_index += 1
            if current_position_index >= len(program):
                break
            current_position = program[current_position_index].linenum
            environment["__program_counter"] = current_position
        else:
            current_position = environment["__program_counter"]
            # Handle GOTO statements
            for i, line in enumerate(program):
                if line.linenum == current_position:
                    current_position_index = i
                    break

        # Find the line with the current program counter
        line = None
        for l in program:
            if l.linenum == environment["__program_counter"]:
                line = l
                break

        if line is None:
            break

        # Execute the line
        if verbose:
            click.echo(f"Executing: {line}")

        # Infinite loops
        if previous_position == current_position and loop_counter > max_loops:
            click.echo("Infinite loop detected. Exiting.", err=True)
            break
        elif previous_position == current_position:
            loop_counter += 1
        else:
            loop_counter = 0

        # Execute the statement
        line.statement.execute(environment)

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
    return classes.Line(line_number, parse_tokens(tokens))

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
        elif char.isspace() and not in_string:
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

    # Assignments
    if keyword == "LET": # LET <variable> = <expression>
        return parse_let_stmt(tokens)
    
    # IO statements
    elif keyword == "PRINT": # PRINT <expression>
        return parse_print_stmt(tokens)
    elif keyword == "INPUT": # INPUT <identifier> <string>
        return parse_input_stmt(tokens)

    # Control flow statements
    elif keyword == "GOTO": # GOTO <value:int>
        return parse_goto_stmt(tokens)
    elif keyword == "IF": # IF <expression> THEN <statement>
        return parse_if_stmt(tokens)
    elif keyword == "ELSE": # ELSE <statement>
        return parse_else_stmt(tokens)
    elif keyword == "END": # END
        return parse_end_stmt(tokens)

    # Loops
    elif keyword == "WHILE": # WHILE <expression> DO <statement>
        raise NotImplementedError("WHILE statement not implemented")
    elif keyword == "FOR": # FOR <identifier> = <expression> TO <expression> [ STEP <expression> ]
        raise NotImplementedError("FOR statement not implemented")
    elif keyword == "NEXT": # NEXT <identifier>
        raise NotImplementedError("NEXT statement not implemented")

    # Comments
    elif keyword == "REM": # REM <...>
        # Ignore comments
        line = ' '.join(tokens)
        return classes.RemStatement(line)

    else:
        raise ValueError(f"Unknown statement: {keyword}")

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

    # Case: VALUE [ OPERATOR EXPRESSION ]
    if len(tokens) >= 1:
        token = tokens.pop(0)
        if token.isdigit():
            left = classes.Value(int(token))
        else:
            # Handle string literals
            if token.startswith('"'):
                while not token.endswith('"'):
                    token += tokens.pop(0)
                left = classes.Value(token[1:-1])
            else:
                # Handle identifiers
                left = classes.Identifier(token)

        if len(tokens) > 1:
            operator = tokens.pop(0)
            right = parse_expression(tokens)
            operation = classes.Operation(operator, left, right)
            return operation
        else:
            return left

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

# PRINT <expression>
def parse_print_stmt(tokens):
    """
    Parse a PRINT statement.
    Args:
        tokens (list): A list of tokens.
    Returns:
        PrintStatement: The parsed PRINT statement.
    """

    line = ' '.join(tokens)
    if len(tokens) == 0:
        raise ValueError("Invalid PRINT statement")

    expression = parse_expression(tokens)

    if expression is None:
        raise ValueError("Invalid PRINT statement")
    return classes.PrintStatement(line, expression)

# INPUT <identifier> <string>
def parse_input_stmt(tokens):
    """
    Parse an INPUT statement.
    Args:
        tokens (list): A list of tokens.
    Returns:
        InputStatement: The parsed INPUT statement.
    """

    line = ' '.join(tokens)

    if len(tokens) == 0:
        raise ValueError("Invalid INPUT statement")
    
    identifier = classes.Identifier(tokens[0])
    prompt = tokens[1] if len(tokens) > 1 else None

    return classes.InputStatement(line, identifier, prompt)

# GOTO <value>
def parse_goto_stmt(tokens):
    """
    Parse a GOTO statement.
    Args:
        tokens (list): A list of tokens.
    Returns:
        GotoStatement: The parsed GOTO statement.
    """
    line = ' '.join(tokens)
    if len(tokens) == 0:
        raise ValueError("Invalid GOTO statement")
    
    line_number = int(tokens[0])
    return classes.GotoStatement(line, line_number)

# IF <expression> GOTO <value>
def parse_if_stmt(tokens):
    """
    Parse an IF statement.
    Args:
        tokens (list): A list of tokens.
    Returns:
        IfStatement: The parsed IF statement.
    """

    line = ' '.join(tokens)
    if len(tokens) < 3:
        raise ValueError("Invalid IF statement")
    goto_index = tokens.index("GOTO")
    if goto_index == -1:
        raise ValueError("Invalid IF statement")

    expression = parse_expression(tokens[:goto_index])
    if expression is None:
        raise ValueError("Invalid IF statement")

    if len(tokens) < goto_index + 2:
        raise ValueError("Invalid IF statement")
    line_number = int(tokens[goto_index + 1])
    return classes.IfStatement(line, expression, line_number)

# ELSE GOTO <value>
def parse_else_stmt(tokens):
    """
    Parse an ELSE statement.
    Args:
        tokens (list): A list of tokens.
    Returns:
        ElseStatement: The parsed ELSE statement.
    """

    line = ' '.join(tokens)
    if len(tokens) == 0:
        raise ValueError("Invalid ELSE statement")

    if tokens[0] != "GOTO":
        raise ValueError("Invalid ELSE statement")

    line_number = int(tokens[1])
    return classes.ElseStatement(line, line_number)

def parse_end_stmt(tokens):
    pass

def parse_while_stmt(tokens):
    pass

def parse_for_stmt(tokens):
    pass

def parse_next_stmt(tokens):
    pass
