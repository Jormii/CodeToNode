class ParsingException(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message


class ReturnException(Exception):

    def __init__(self, value):
        super().__init__()
        self.value = value
