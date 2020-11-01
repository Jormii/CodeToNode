import time


class Callable:

    def arity(self):
        raise NotImplementedError()

    def call(self, interpreter, arguments):
        raise NotImplementedError()


class CustomFunction(Callable):

    def __init__(self, declaration):
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.parameters)

    def call(self, interpreter, arguments):
        previous_environment = interpreter.environment
        new_environment = previous_environment.copy()

        for i in range(self.arity()):
            parameter = self.declaration.parameters[i]
            argument = arguments[i]

            new_environment.define(parameter.lexeme, argument)

        interpreter.environment = new_environment
        interpreter.execute_block(self.declaration.body)
        interpreter.environment = previous_environment
        return None


class ClockCall(Callable):

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time() / 1000.0
