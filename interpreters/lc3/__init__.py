"""
interpreters/lc3
LC-3 (Little Computer 3) interpreter
"""

# WARNING: This code is not complete. LC-3 interpretation does not work properly.

import interpreters.lc3.environment as environment

def run(file, verbose=False):
    """
    Run the LC-3 interpreter on a given file.

    Args:
        file (str): Path to the LC-3 assembly file.
        verbose (bool): If True, enable verbose output.
    """

    # Initialize the LC-3 environment
    environment.reset_environment()

    with open(file, 'r') as f:
        lines = f.readlines()

    # Find .ORIG line first, and set program counter
    line = lines.pop(0)
    while not line.startswith('.ORIG'):
        line = lines.pop(0)
        if line.strip() == '':
            continue
        if line.startswith(';'):
            continue

        if line.startswith('.FILL'):
            raise ValueError(".FILL directive found before .ORIG.")
        if line.startswith('.STRINGZ'):
            raise ValueError(".STRINGZ directive found before .ORIG.")
        if line.startswith('.BLKW'):
            raise ValueError(".BLKW directive found before .ORIG.")
        if line.startswith('.END'):
            raise ValueError(".END directive found before .ORIG.")
    
    # Parse the .ORIG line
    orig_line = line.split()
    if len(orig_line) != 2:
        raise ValueError("Invalid .ORIG line format.")
    if not orig_line[1].startswith('x'):
        raise ValueError(".ORIG address must be in hexadecimal format.")
    try:
        environment.program_counter = int(orig_line[1][1:], 16)
        environment.program_start = int(orig_line[1][1:], 16)
    except ValueError:
        raise ValueError("Invalid .ORIG address format.")

    for line in lines:
        if line.strip() == '':
            continue
        if line.startswith(';'):
            continue

        # Parse the line and execute the instruction
        statement = parse_line(line)
        if statement is None:
            continue

        click.echo(f"Statement: {statement}")

    pass

def parse_line(line):
    """
    Parse a line of LC-3 assembly code.
    
    Args:
        line (str): A line of LC-3 assembly code.
        
    Returns:
        Statement: A Statement object representing the parsed line.
    """

    tokens = line.split()
    if not tokens:
        return None

    for token in tokens:
        if token.startswith(';'):
            break # Ignore comments


