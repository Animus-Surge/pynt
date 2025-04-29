"""
interpreters/lc3/classes.py
LC-3 interpreter classes
"""

class Value:
    """
    A class representing a LC-3 value.
    
    Attributes:
        value (any): The value of the expression.
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Value({self.value})"

    def evaluate(self, environment):
        """
        Evaluate the value.
        """
        return self.value

class Register(Value):
    """
    A class representing a LC-3 register.
    
    Attributes:
        index (int): The index of the register (0-7).
    """

    def __init__(self, index):
        if not (0 <= index <= 7):
            raise ValueError("Register index must be between 0 and 7.")
        self.index = index

    def __repr__(self):
        return f"Register({self.index})"

class Immediate(Value):
    """
    A class representing a LC-3 immediate value.
    
    Attributes:
        value (int): The immediate value.
    """

    def __init__(self, value):
        if not (-32768 <= value <= 32767):
            raise ValueError("Immediate value must be between -32768 and 32767.")
        self.value = value

    def __repr__(self):
        return f"Immediate({self.value})"
        self.value = value

class Address(Value):
    """
    A class representing a LC-3 address.
    
    Attributes:
        address (int): The address value.
    """

    def __init__(self, address):
        if not (0 <= address <= 65535):
            raise ValueError("Address must be between 0 and 65535.")
        self.address = address

    def __repr__(self):
        return f"Address({self.address})"

class Label(Value):
    """
    A class representing a LC-3 label.
    
    Attributes:
        name (str): The name of the label.
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Label({self.name})"

    def evaluate(self, environment):
        """
        Evaluate the label.
        """
        # Assuming environment has a method to get address by label name
        return environment.get_address_by_label(self.name)

class Statement:
    """
    A class representing a LC-3 statement.
    
    Attributes:
        opcode (str): The opcode of the statement.
        op1 (str): The first operand of the statement.
        op2 (str): The second operand of the statement.
        op3 (str): The third operand of the statement.
    """

    def __init__(self, opcode, op1=None, op2=None, op3=None):
        self.opcode = opcode
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return f"Statement({self.opcode}, {self.op1}, {self.op2}, {self.op3})"

    def execute(self):
        """
        Execute the statement in the given environment.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class AddStatement(Statement):
    """
    A class representing an ADD statement in LC-3.
    
    Attributes:
        dest (Register): The destination register.
        src1 (Register): The first source register.
        src2 (Value): The second source value (register or immediate).
    """

    def __init__(self, dest, src1, src2):
        super().__init__('ADD', dest, src1, src2)
        self.dest = dest
        self.src1 = src1
        self.src2 = src2

    def execute(self)
        """
        Execute the ADD statement.
        """
        # Assuming environment has a method to get register value
        src1_value = self.src1.evaluate(environment)
        if isinstance(self.src2, Register):
            src2_value = self.src2.evaluate(environment)
        else:
            src2_value = self.src2.value

        result = (src1_value + src2_value) & 0xFFFF  # Mask to 16 bits
        environment.set_register(self.dest.index, result)



class AndStatement(Statement):
    """
    A class representing an AND statement in LC-3.
    
    Attributes:
        dest (Register): The destination register.
        src1 (Register): The first source register.
        src2 (Value): The second source value (register or immediate).
    """

    def __init__(self, dest, src1, src2):
        super().__init__('AND', dest, src1, src2)
        self.dest = dest
        self.src1 = src1
        self.src2 = src2

    def execute(self):
        """
        Execute the AND statement.
        """
        # Assuming environment has a method to get register value
        src1_value = self.src1.evaluate(environment)
        if isinstance(self.src2, Register):
            src2_value = self.src2.evaluate(environment)
        else:
            src2_value = self.src2.value

        result = (src1_value & src2_value) & 0xFFFF
        environment.set_register(self.dest.index, result)

class NotStatement(Statement):
    """
    A class representing a NOT statement in LC-3.
    
    Attributes:
        dest (Register): The destination register.
        src (Register): The source register.
    """

    def __init__(self, dest, src):
        super().__init__('NOT', dest, src)
        self.dest = dest
        self.src = src

    def execute(self):
        """
        Execute the NOT statement.
        """
        # Assuming environment has a method to get register value
        src_value = self.src.evaluate(environment)
        result = (~src_value) & 0xFFFF

class TrapStatement(Statement):
    """
    A class representing a TRAP statement in LC-3.
    
    Attributes:
        trap_vector (int): The trap vector.
    """

    def __init__(self, trap_vector):
        super().__init__('TRAP', trap_vector)
        self.trap_vector = trap_vector

    def execute(self):
        """
        Execute the TRAP statement.
        """
        # Assuming environment has a method to execute trap
        environment.execute_trap(self.trap_vector)

