from transpiler.callable_c2n import Callable
from transpiler.logger_c2n import log_error, ErrorStep


class Environment:

    def __init__(self, filename):
        self.filename = filename
        self.values = {}
        self.indentation_level = 0

    def define(self, name, value):
        is_function = isinstance(value, Callable)
        if self.indentation_level == 0 and not is_function:
            log_error(
                self.filename, name.line, ErrorStep.RUNTIME, "Error with variable \"{}\". Global variables aren't supported".format(name))

        if self.indentation_level != 0 and is_function:
            log_error(self.filename, name.line, ErrorStep.RUNTIME,
                      "Local functions aren't supported")

        # Functions cannot be overriden
        if is_function and name.lexeme in self.values:
            log_error(self.filename, name.line, ErrorStep.RUNTIME,
                      "Function \"{}\" was already defined".format(name.lexeme))

        self.values[name.lexeme] = value

    def get(self, token):
        name = token.lexeme
        if name in self.values:
            return self.values[name]

        log_error(self.filename, token.line, ErrorStep.RUNTIME,
                  "Undefined variable \"{}\"".format(name))

    def new_block(self):
        self.indentation_level += 1

    def end_of_block(self):
        self.indentation_level -= 1
        if self.indentation_level == 0:
            self.clear_non_functions()

    def clear_non_functions(self):
        # Functions are defined in global namespace. When reaching the end of a full block,
        # non-functions have to be deleted

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
