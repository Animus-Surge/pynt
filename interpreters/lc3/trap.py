"""
interpreters/lc3/trap.py
LC-3 trap functions
"""

import click

def trap_GETC():
    pass

def trap_OUT():
    pass

def trap_PUTS():
    """
    Print a string to the console.
    
    The string is expected to be null-terminated.
    """
    # Read the address of the string from R0
    address = registers[0]
    
    # Read characters until we hit a null terminator
    while True:
        char = memory[address]
        if char == 0:
            break
        click.echo(char, nl=False)
        address += 1

def trap_IN():
    """
    Read a character from the keyboard and echo it to the console.
    """
    # Read a character from the keyboard
    char = click.prompt("", type=str, default='', show_default=False, prompt_suffix='')
    
    # Store the character in R0
    registers[0] = ord(char[0]) if char else 0
    
    # Echo the character to the console
    click.echo(char, nl=False)

def trap_PUTSP():
    pass

def trap_HALT():
    pass

trap_table = {
    0x20: trap_GETC,
    0x21: trap_OUT,
    0x22: trap_PUTS,
    0x23: trap_IN,
    0x24: trap_PUTSP,
    0x25: trap_HALT
}
