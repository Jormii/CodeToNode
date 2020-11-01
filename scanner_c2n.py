import sys
import keyword
import numpy as np

from token_c2n import Token, TokenType
from logger_c2n import log_error, ErrorStep


class Scanner:

    # Keywords supported and their token types
    keywords = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "True": TokenType.TRUE,
        "False": TokenType.FALSE,
        "while": TokenType.WHILE,
        "None": TokenType.NONE,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "def": TokenType.DEF,
        "return": TokenType.RETURN,
        "from": TokenType.FROM,
        "import": TokenType.IMPORT
    }

    unsupported_keywords = set(keyword.kwlist) - set(keywords.keys())

    def __init__(self, filename, source_code):
        self.filename = filename
        self.source = source_code
        self.indentations = [0]
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.found_character = False

    def perform_scanning(self):
        self.calculate_indentations()

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.check_for_semicolon()
        self.add_final_right_curly_braces()
        self.tokens.append(Token(TokenType.EOF, self.line))
        return self.tokens

    def calculate_indentations(self):
        found_character = False
        found_spaces = False
        for c in self.source:
            if c == "\n":
                found_character = False
                self.indentations.append(0)
            elif c in " \t":
                if found_character:
                    continue

                self.indentations[-1] += 1

                if c == " ":
                    found_spaces = True
            else:
                found_character = True

        if found_spaces:
            self.translate_spaces_to_tabs()

    def translate_spaces_to_tabs(self):
        indentations_np = np.array(self.indentations)
        indentations_np_no_zeros = np.where(
            indentations_np == 0, sys.maxsize, indentations_np)
        minimum = np.min(indentations_np_no_zeros)

        modulo = indentations_np % minimum
        for i in range(len(modulo)):
            if modulo[i] != 0:
                log_error(self.filename, i, ErrorStep.SCANNING,
                          "Indentation error")

        tabs = indentations_np // minimum
        self.indentations = tabs.tolist()

    def scan_token(self):
        c = self.advance()

        if c in " \t\r":
            return
        if c == "\n":
            if self.found_character:
                self.check_for_right_curly_braces()
                self.found_character = False
            self.check_for_semicolon()
            self.line += 1
            return

        self.found_character = True

        if c == "(":
            self.add_token(TokenType.LEFT_PARENTHESIS)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PARENTHESIS)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ":":
            self.add_left_curly_brace()
        elif c == "+":
            self.add_token(TokenType.ADD)
        elif c == "-":
            self.add_token(TokenType.SUBSTRACT)
        elif c == "%":
            self.add_token(TokenType.MODULUS)

        elif c == "*":
            next_is_asterisk = self.next_matches("*")
            token_type = TokenType.POWER if next_is_asterisk else TokenType.PRODUCT
            self.add_token(token_type)
        elif c == "/":
            next_is_slash = self.next_matches("/")
            token_type = TokenType.FLOOR_DIVISION if next_is_slash else TokenType.DIVISION
            self.add_token(token_type)
        elif c == "!":
            next_is_equal = self.next_matches("=")
            if not next_is_equal:
                log_error(self.filename, self.line, ErrorStep.SCANNING,
                          "! character doesn't precede =")

            self.add_token(TokenType.NOT_EQUAL)
        elif c == "=":
            next_is_equal = self.next_matches("=")
            token_type = TokenType.EQUAL if next_is_equal else TokenType.ASSIGMENT
            self.add_token(token_type)
        elif c == "<":
            next_is_equal = self.next_matches("=")
            token_type = TokenType.LESS_OR_EQUAL if next_is_equal else TokenType.LESS_THAN
            self.add_token(token_type)
        elif c == ">":
            next_is_equal = self.next_matches("=")
            token_type = TokenType.GREATER_OR_EQUAL if next_is_equal else TokenType.GREATER_THAN
            self.add_token(token_type)

        elif c == "#":
            while self.peek() != "\n" and not self.is_at_end():
                self.advance()
        elif c.isnumeric():
            self.scan_number()
        elif self.is_alphabetic(c):
            self.scan_identifier()
        else:
            log_error(self.filename, self.line, ErrorStep.SCANNING,
                      "Unexpected character \"{}\"".format(c))

    def is_at_end(self):
        return self.current >= len(self.source)

    def peek(self):
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def peek_next(self):
        if (self.current + 1) >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def next_matches(self, character):
        if self.is_at_end():
            return False

        if self.source[self.current] != character:
            return False

        self.current += 1
        return True

    def scan_number(self):
        while self.peek().isnumeric():
            self.advance()

        # Look for decimal dot
        if self.peek() == "." and self.peek_next().isnumeric():
            self.advance()

            while self.peek().isnumeric():
                self.advance()

        number_substring = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, float(number_substring))

    def scan_identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        identifier = self.source[self.start:self.current]

        if identifier in Scanner.unsupported_keywords:
            log_error(self.filename, self.line, ErrorStep.SCANNING,
                      "Found unsupported keyword \"{}\"".format(identifier))

        token_type = TokenType.IDENTIFIER if identifier not in Scanner.keywords else Scanner.keywords[
            identifier]

        # Ignore "from" and "import" statements
        if token_type in [TokenType.FROM, TokenType.IMPORT]:
            while self.peek() != "\n" and not self.is_at_end():
                self.advance()
            return

        self.add_token(token_type)

    def add_token(self, token_type, literal=None):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, self.line, lexeme, literal))

    def add_left_curly_brace(self):
        self.tokens.append(Token(TokenType.LEFT_CURLY_BRACE, self.line, "{"))

    def check_for_right_curly_braces(self):
        previous_token = self.find_previous_token()
        if previous_token is None:
            return

        last_token_line = previous_token.line
        previous_indentation_level = self.indentations[last_token_line - 1]
        this_line_indentation_level = self.indentations[self.line - 1]

        if this_line_indentation_level < previous_indentation_level:
            difference = previous_indentation_level - this_line_indentation_level
            for i in range(difference):
                self.add_right_curly_brace(last_token_line)

    def find_previous_token(self):
        for i in range(len(self.tokens) - 1, -1, -1):
            token_i = self.tokens[i]
            if token_i.line < self.line:
                return token_i

        return None

    def add_right_curly_brace(self, line):
        token = Token(TokenType.RIGHT_CURLY_BRACE, line, "}")
        for i in range(len(self.tokens) - 1, -1, -1):
            token_i = self.tokens[i]
            if token_i.line == line:
                self.tokens.insert(i + 1, token)
                return

    def add_final_right_curly_braces(self):
        if len(self.tokens) == 0:
            return

        last_token_line = self.tokens[-1].line
        previous_indentation_level = self.indentations[last_token_line - 1]
        for i in range(previous_indentation_level):
            self.add_right_curly_brace(last_token_line)

    def check_for_semicolon(self):
        if len(self.tokens) == 0:
            return

        previous_token = self.tokens[-1]
        token_type = previous_token.token_type
        line = previous_token.line

        if line == self.line and token_type != TokenType.LEFT_CURLY_BRACE:
            semicolon_token = Token(TokenType.SEMICOLON, self.line, ";")
            self.tokens.append(semicolon_token)

    def is_alphabetic(self, c):
        return c.isalpha() or c == "_"

    def is_alphanumeric(self, c):
        return c.isnumeric() or self.is_alphabetic(c)
