"""
interpreters/basic/classes.py
BASIC interpreter classes
"""

import click

class Expression:
    """
    A class representing a BASIC expression.
    
    Attributes:
        expression (str): The expression string.
    """

    def __init__(self):
        pass

    def __repr__(self):
        return f"Expression()"
            
    def evaluate(self, environment):
        """
        Evaluate the expression.
        """
        raise NotImplementedError("Expression evaluation must be implemented in subclasses.")

class Value(Expression):
    """
    A class representing a BASIC value.
    
    Attributes:
        value (any): Value of the expression.
    """

    def __init__(self, value):
        super().__init__()

        # Strip leading and trailing quotes
        if isinstance(value, str):
            value = value.strip('"').strip("'")
            try:
                value = int(value)
            except ValueError:
                pass
        self.value = value

    def __repr__(self):
        return f"Value({self.value})"

    def evaluate(self, environment):
        """
        Evaluate the value.
        """
        return self.value

class Identifier(Value):
    """
    A class representing a BASIC identifier.
    
    Attributes:
        name (str): The name of the identifier.
    """

    def __init__(self, name):
        super().__init__(None)
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

    def evaluate(self, environment):
        """
        Evaluate the identifier.
        """
        if self.value:
            return self.value

        if self.name in environment:
            self.value = environment[self.name]
            return environment[self.name]
        else:
            raise NameError(f"Undefined variable: {self.name}")

class Operation(Expression):
    """
    A class representing a BASIC operation.

    Attributes:
        operator (str): The operator for the operation.
        left (Expression): The left operand.
        right (Expression): The right operand.
    """
    
    def __init__(self, operator, left, right):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, environment):
        """
        Evaluate the operation.
        """

        # Evaluate the left and right operands
        left_value = self.left.evaluate(environment)
        right_value = self.right.evaluate(environment)

        result = 0

        # Arithmetic operations
        if self.operator == '+':
            result = left_value + right_value
        elif self.operator == '-':
            result = left_value - right_value
        elif self.operator == '*':
            result = left_value * right_value
        elif self.operator == '/':
            result = left_value / right_value

        # Logical operations
        elif self.operator == '==':
            result = left_value == right_value
        elif self.operator == '<':
            result = left_value < right_value
        elif self.operator == '>':
            result = left_value > right_value
        elif self.operator == '<=':
            result = left_value <= right_value
        elif self.operator == '>=':
            result = left_value >= right_value
        elif self.operator == '!=':
            result = left_value != right_value

        else:
            raise ValueError(f"Invalid operator: {self.operator}")

        if environment["__verbose"]:
            click.echo(f"Evaluated: {self.left} {self.operator} {self.right} = {result}")

        return result

    def __repr__(self):
        return f"Operation({self.left} {self.operator} {self.right})"

class Line:
    """
    A class representing a BASIC line.
    
    Attributes:
        linenum (int): The line number.
        statement (Statement): The statement string.
    """

    def __init__(self, linenum, statement):
        self.linenum = linenum
        self.statement = statement

    def __repr__(self):
        return f"{self.linenum}: {self.statement}"

    def evaluate(self, environment):
        """
        Evaluate the line.
        """
        if isinstance(self.statement, Statement):
            self.statement.execute(environment)
        else:
            raise TypeError("Statement must be an instance of Statement class.")

class Statement:
    """
    Base class for BASIC statements.
    """

    def __init__(self, line):
        self.line = line

    def __repr__(self):
        return f"Statement({self.line})"

    def execute(self, environment):
        """
        Execute the statement.
        """
        raise NotImplementedError("Statement execution must be implemented in subclasses.")

class RemStatement(Statement):
    """
    A class representing a REM statement.
    
    Attributes:
        comment (str): The comment string.
    """

    def __init__(self, line):
        super().__init__(line)

    def __repr__(self):
        return f"RemStatement()"

    def execute(self, environment):
        """
        Execute the REM statement.
        """
        pass

class PrintStatement(Statement):
    """
    A class representing a PRINT statement.
    
    Attributes:
        expression (Expression): The expression to print.
    """

    def __init__(self, line, expression):
        super().__init__(line)
        self.expression = expression

    def __repr__(self):
        return f"PrintStatement({self.expression})"

    def execute(self, environment):
        """
        Execute the PRINT statement.
        """
        value = self.expression.evaluate(environment)
        click.echo(value)

class InputStatement(Statement):
    """
    A class representing an INPUT statement.
    
    Attributes:
        identifier (Identifier): The identifier to store the input value.
    """

    def __init__(self, line, identifier, prompt=None):
        super().__init__(line)
        self.identifier = identifier

        if prompt:
            # Strip leading and trailing quotes or whitespace
            prompt = prompt.strip().strip('"').strip("'")

        self.prompt = prompt

    def __repr__(self):
        return f"InputStatement({self.identifier}, {self.prompt})"

    def execute(self, environment):
        """
        Execute the INPUT statement.
        """
        value = click.prompt(self.prompt if self.prompt else "", type=str)

        # Automatically cast to number if possible
        try:
            value = int(value)
        except ValueError:
            pass # Ignore error
        finally:
            environment[self.identifier.name] = value

class GotoStatement(Statement):
    """
    A class representing a GOTO statement.
    
    Attributes:
        line_number (int): The line number to go to.
    """

    def __init__(self, line, line_number):
        super().__init__(line)
        self.line_number = line_number

    def __repr__(self):
        return f"GotoStatement({self.line_number})"

    def execute(self, environment):
        """
        Execute the GOTO statement.
        """
        # Set the program counter to the specified line number
        environment['__program_counter'] = self.line_number

        if environment["__verbose"]:
            click.echo(f"GOTO {self.line_number}")

class LetStatement(Statement):
    """
    A class representing a LET statement.
    
    Attributes:
        identifier (Identifier): The identifier to assign the value to.
        expression (Expression): The expression to evaluate and assign.
    """

    def __init__(self, line, identifier, expression):
        super().__init__(line)
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"LetStatement({self.identifier}, {self.expression})"

    def execute(self, environment):
        """
        Execute the LET statement.
        """
        value = self.expression.evaluate(environment)
        environment[self.identifier.name] = value

        if environment["__verbose"]:
            click.echo(f"LET {self.identifier.name} = {value}")

class IfStatement (Statement): # IF <expression> GOTO <line_number>
    """
    A class representing an IF statement.
    
    Attributes:
        condition (Expression): The condition to evaluate.
        line_number (int): The line number to go to if the condition is true.
    """

    def __init__(self, line, condition, line_number):
        super().__init__(line)
        self.condition = condition
        self.line_number = line_number

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.line_number})"

    def execute(self, environment):
        """
        Execute the IF statement.
        """
        if self.condition.evaluate(environment):
            environment['__program_counter'] = self.line_number

class ElseStatement(Statement):
    """
    A class representing an ELSE statement.
    
    Attributes:
        line_number (int): The line number to go to if the condition is false.
    """

    def __init__(self, line, line_number):
        super().__init__(line)
        self.line_number = line_number

    def __repr__(self):
        return f"ElseStatement({self.line_number})"

    def execute(self, environment):
        """
        Execute the ELSE statement.
        """
        environment['__program_counter'] = self.line_number
