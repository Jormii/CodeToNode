from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    WHILE = auto()  # Although while is implemented in the transpiler, it's not supported in terms of Blender nodes yet
    NONE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    DEF = auto()
    RETURN = auto()
    FROM = auto()       # Although from and import are recognized, these are ignored. Therefore, importing isn't allowed
    IMPORT = auto()

    # Arithmetic operators
    ADD = auto()
    SUBSTRACT = auto()
    PRODUCT = auto()
    DIVISION = auto()
    FLOOR_DIVISION = auto()
    MODULUS = auto()
    POWER = auto()

    # Comparison operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_OR_EQUAL = auto()
    LESS_THAN = auto()
    LESS_OR_EQUAL = auto()

    # Assigment operators
    ASSIGMENT = auto()

    # Other symbols
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    DOT = auto()
    COMMA = auto()
    LEFT_CURLY_BRACE = auto()       # {} aren't Python symbols but the scanner
    RIGHT_CURLY_BRACE = auto()      # adds these tokens to ease the parsing later

    # Literals
    IDENTIFIER = auto()
    NUMBER = auto()

    # Other
    SEMICOLON = auto()              # Same reason as {}
    EOF = auto()

    # TODO: Not yet supported
    # ELIF = auto()

    # TODO: Consider the following
    # BITWISE_AND = auto()
    # BITWISE_OR = auto()
    # BITWISE_NOT = auto()
    # BITSISE_XOR = auto()
    # BITWISE_RIGHT_SHIFT = auto()
    # BITWISE_LEFT_SHIFT = auto()

    # ASSIGMENT_ADD = auto()
    # ASSIGMENT_SUBSTRACT = auto()
    # ASSIGMENT_PRODUCT = auto()
    # ASSIGMENT_DIVISION = auto()
    # ASSIGMENT_MODULUS = auto()
    # ASSIGMENT_FLOOR_DIVISION = auto()
    # ASSIGMENT_POWER = auto()
    # ASSIGMENT_BITWISE_AND = auto()
    # ASSIGMENT_BITWISE_OR = auto()
    # ASSIGMENT_BITWISE_XOR = auto()
    # ASSIGMENT_BITWISE_RIGHT_SHIFT = auto()
    # ASSIGMENT_BITWISE_LEFT_SHIFT = auto()

    # IN = auto()
    # LEFT_BOX_BRACKET = auto()
    # RIGHT_BOX_BRACKET = auto()

    # GLOBAL = auto()
    # STRING = auto()

    # FOR = auto()
    # BREAK = auto()
    # CONTINUE = auto()

    # Keywords that won't be added:
    # is


class Token:

    def __init__(self, token_type, line, lexeme="", literal=None):
        self.token_type = token_type
        self.line = line
        self.lexeme = lexeme
        self.literal = literal

    def to_string(self):
        return "Token {}: Lexeme: \"{}\", Literal: \"{}\", Line: {}".format(self.token_type.name, self.lexeme, self.literal, self.line)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()
