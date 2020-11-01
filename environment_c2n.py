from logger_c2n import log_error
from callable_c2n import Callable


class Environment:

    def __init__(self, filename):
        self.filename = filename
        self.values = {}
        self.indentation_level = 0

    def define(self, name, value):
        # TODO: Pass token as argument
        is_function = isinstance(value, Callable)
        if self.indentation_level == 0 and not is_function:
            log_error(
                self.filename, -1, "Error with variable \"{}\". Global variables aren't supported".format(name))

        self.values[name] = value

    def assign(self, token, value):
        name = token.lexeme
        is_function = isinstance(value, Callable)

        if self.indentation_level == 0 and not is_function:
            log_error(
                self.filename, token.line, "Error with variable \"{}\". Global variables aren't supported".format(name))

        if name in self.values:
            self.values[name] = value
            return

        log_error(self.filename, token.line,
                  "Undefined variable \"{}\"".format(name))

    def get(self, token):
        name = token.lexeme
        if name in self.values:
            return self.values[name]

        log_error(self.filename, token.line,
                  "Undefined variable \"{}\"".format(name))

    def new_block(self):
        self.indentation_level += 1

    def end_of_block(self):
        self.indentation_level -= 1
        if self.indentation_level == 0:
            self.clear_non_functions()

    def clear_non_functions(self):
        functions = []
        for key, value in self.values.items():
            if isinstance(value, Callable):
                functions.append((key, value))

        self.values.clear()
        for func in functions:
            key = func[0]
            value = func[1]
            self.values[key] = value

    def copy(self):
        copy = Environment(self.filename)
        copy.values = self.values.copy()
        copy.indentation_level = self.indentation_level

        copy.clear_non_functions()

        return copy
