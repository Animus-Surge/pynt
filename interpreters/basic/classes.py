"""
interpreters/basic/classes.py
BASIC interpreter classes
"""

class Statement:
    """
    A class representing a BASIC statement.
    
    Attributes:
        line_number (int): The line number of the statement.
        statement (str): The code for the line
    """

    def __init__(self, line_number, statement):
        self.line_number = line_number
        self.statement = statement

    def __str__(self) -> str:
        return f"{self.line_number} {self.statement}"

    def __repr__(self) -> str:
        return f"Statement({self.line_number}, {self.statement})"
       

    
