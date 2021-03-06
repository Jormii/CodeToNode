from exception_c2n import ReturnException


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

            new_environment.define(parameter, argument)

        value_to_return = None
        try:
            interpreter.environment = new_environment
            interpreter.execute_block(self.declaration.body)
        except ReturnException as exc:
            value_to_return = exc.value
        finally:
            interpreter.environment = previous_environment

        return value_to_return
