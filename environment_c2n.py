from logger_c2n import log_error


class Environment:

    def __init__(self, filename):
        self.filename = filename
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, token):
        name = token.lexeme
        if name in self.values:
            return self.values[name]

        log_error(self.filename, token.line,
                  "Undefined variable \"{}\"".format(name))
