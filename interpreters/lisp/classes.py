"""
interpreters/lisp/classes.py
LISP interpreter classes
"""

import click

class LispExpression:
    def __init__(self):
        pass

    def __str__(self):
        return f"LispExpression()"
    def __repr__(self):
        return f"LispExpression()"

    def evaluate(self, environment):
        raise NotImplementedError("Subclasses should implement this method")

class LispAtom(LispExpression):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"LispAtom({self.value})"
    def __repr__(self):
        return f"LispAtom({self.value})"

    def evaluate(self, environment):
        return self.value

class LispSymbol(LispExpression):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"LispSymbol({self.name})"
    def __repr__(self):
        return f"LispSymbol({self.name})"

    def evaluate(self, environment):
        return environment.get(self.name, None)

class LambdaFunction:
    def __init__(self, params, body, environment):
        self.params = params
        self.body = body
        self.environment = environment

    def __call__(self, *args):
        if len(args) != len(self.params):
            raise ValueError("Incorrect number of arguments")

        local_env = self.environment.copy()
        for param, arg in zip(self.params, args):
            local_env[param.name] = arg

        return self.body.evaluate(local_env)

class LispList(LispExpression):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def __str__(self):
        return f"LispList({self.elements})"
    def __repr__(self):
        return f"LispList({self.elements})"

    def evaluate(self, environment):
        if len(self.elements) == 0:
            return None

        first_element = self.elements[0]

        print(f"Evaluating: {self.elements}")

        if isinstance(first_element, LispSymbol):
            if first_element.name == "define":
                return self.evaluate_define(environment)
            elif first_element.name == "if":
                return self.evaluate_if(environment)
            elif first_element.name == "quote":
                return self.evaluate_quote(environment)
            elif first_element.name == "print":
                return self.evaluate_print(environment)
        

        return self.evaluate_function_call(environment)

    def evaluate_define(self, environment):
        click.echo(self.elements)
        if len(self.elements) != 3:
            raise ValueError("Invalid define syntax")

        if environment["__interpreter_verbose"]:
            click.echo(f"Evaluating define: {self.elements[1]} = {self.elements[2]}")
        
        func = self.elements[1].evaluate(environment)
        value = self.elements[2].evaluate(environment)
        environment[name] = value
        return value

    def evaluate_if(self, environment):
        if len(self.elements) != 4:
            raise ValueError("Invalid if syntax")

        if environment["__interpreter_verbose"]:
            click.echo(f"Evaluating if: {self.elements[1]}")
        
        condition = self.elements[1].evaluate(environment)
        if condition:
            return self.elements[2].evaluate(environment)
        else:
            return self.elements[3].evaluate(environment)

    def evaluate_lambda(self, environment):
        if len(self.elements) != 3:
            raise ValueError("Invalid lambda syntax")

        if environment["__interpreter_verbose"]:
            click.echo(f"Evaluating lambda: {self.elements[1]} -> {self.elements[2]}")

        params = self.elements[1].elements
        body = self.elements[2]
        return LambdaFunction(params, body, environment)
        
    def evaluate_quote(self, environment):
        if len(self.elements) != 2:
            raise ValueError("Invalid quote syntax")

        if environment["__interpreter_verbose"]:
            click.echo(f"Evaluating quote: {self.elements[1]}")
        
        return self.elements[1]

    def evaluate_function_call(self, environment):
        function = self.elements[0].evaluate(environment)
        args = [element.evaluate(environment) for element in self.elements[1:]]

        if environment["__interpreter_verbose"]:
            click.echo(f"Evaluating function call: {function} with args: {args}")
        
        if callable(function):
            return function(*args)
        else:
            raise ValueError(f"{function} is not a callable function")

    def evaluate_print(self, environment):
        if len(self.elements) != 2:
            raise ValueError("Invalid print syntax")

        if environment["__interpreter_verbose"]:
            click.echo(f"Evaluating print: {self.elements[1]}")
        
        value = self.elements[1].evaluate(environment)
        click.echo(value)
        return value
