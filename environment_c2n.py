from logger_c2n import log_error


class Environment:

    def __init__(self, filename):
        self.filename = filename
        self.values = {}
        self.indentation_level = 0

    def define(self, name, value):
        # TODO: Pass token as argument
        if self.indentation_level == 0:
            log_error(
                self.filename, -1, "Error with variable \"{}\". Global variables aren't supported".format(name))

        self.values[name] = value

    def assign(self, token, value):
        name = token.lexeme

        if self.indentation_level == 0:
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
            self.values.clear()
