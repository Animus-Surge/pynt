"""
interpreters/lc3/environment.py
LC-3 interpreter environment
"""

import click

import interpreters.lc3.trap as trap

program_counter = 0
program_start = 0

memory = [None] * 65536
registers = [0] * 8
flags = {
    "N": 0,
    "Z": 0,
    "P": 0
}

def reset_environment():
    """
    Reset the LC-3 environment to its initial state.
    """
    global program_counter
    global memory
    global registers
    global flags

    program_counter = 0
    memory = [None] * 65536
    registers = [0] * 8
    flags = {
        "N": 0,
        "Z": 0,
        "P": 0
    }

def pc_increment():
    """
    Increment the program counter.
    """
    global program_counter
    program_counter = (program_counter + 1) % 65536

def set_flag(flag, value):
    """
    Set a flag in the flags dictionary.
    
    Args:
        flag (str): The flag to set ('N', 'Z', or 'P').
        value (int): The value to set the flag to (0 or 1).
    """
    global flags
    if flag in flags:
        flags[flag] = value
    else:
        raise ValueError(f"Invalid flag: {flag}")

def get_flag(flag):
    """
    Get the value of a flag in the flags dictionary.
    
    Args:
        flag (str): The flag to get ('N', 'Z', or 'P').
        
    Returns:
        int: The value of the flag (0 or 1).
    """
    global flags
    if flag in flags:
        return flags[flag]
    else:
        raise ValueError(f"Invalid flag: {flag}")

def set_register(index, value):
    """
    Set a value in the registers list.
    
    Args:
        index (int): The index of the register (0-7).
        value (int): The value to set the register to.
    """
    global registers
    if 0 <= index < len(registers):
        registers[index] = value
    else:
        raise ValueError(f"Invalid register index: {index}")

def get_register(index):
    """
    Get the value of a register in the registers list.
    
    Args:
        index (int): The index of the register (0-7).
        
    Returns:
        int: The value of the register.
    """
    global registers
    if 0 <= index < len(registers):
        return registers[index]
    else:
        raise ValueError(f"Invalid register index: {index}")

def set_memory(address, value):
    """
    Set a value in the memory list.
    
    Args:
        address (int): The address in memory (0-65535).
        value (int): The value to set the memory location to.
    """
    global memory
    if 0 <= address < len(memory):
        memory[address] = value
    else:
        raise ValueError(f"Invalid memory address: {address}")

def get_memory(address):
    """
    Get the value of a memory location in the memory list.
    
    Args:
        address (int): The address in memory (0-65535).
        
    Returns:
        int: The value at the memory location.
    """
    global memory
    if 0 <= address < len(memory):
        return memory[address]
    else:
        raise ValueError(f"Invalid memory address: {address}")


def execute_trap(trap_vector):
    """
    Execute a trap function based on the given trap vector.
    
    Args:
        trap_vector (int): The trap vector to execute.
    """
    if trap_vector in trap.trap_table:
        trap.trap_table[trap_vector]()
    else:
        raise ValueError(f"Invalid trap vector: {trap_vector}")
