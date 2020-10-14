from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    TRUE = auto()
    FALSE = auto()
    NONE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    DEF = auto()
    RETURN = auto()
    FROM = auto()
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
    COLON = auto()

    # Literals
    IDENTIFIER = auto()
    NUMBER = auto()

    # Other
    EOF = auto()

    # TODO: Not yet supported
    # IF = 103
    # ELIF = 104
    # ELSE = 105
    
    # TODO: Consider
    # BITWISE_AND = 30
    # BITWISE_OR = 31
    # BITWISE_NOT = 32
    # BITSISE_XOR = 33
    # BITWISE_RIGHT_SHIFT = 34
    # BITWISE_LEFT_SHIFT = 35
    # ASSIGMENT_ADD = 41
    # ASSIGMENT_SUBSTRACT = 42
    # ASSIGMENT_PRODUCT = 43
    # ASSIGMENT_DIVISION = 44
    # ASSIGMENT_MODULUS = 45
    # ASSIGMENT_FLOOR_DIVISION = 46
    # ASSIGMENT_POWER = 47
    # ASSIGMENT_BITWISE_AND = 48
    # ASSIGMENT_BITWISE_OR = 49
    # ASSIGMENT_BITWISE_XOR = 50
    # ASSIGMENT_BITWISE_RIGHT_SHIFT = 51
    # ASSIGMENT_BITWISE_LEFT_SHIFT = 52
    # IS = 60
    # IS_NOT = 61
    # IN = 70
    # NOT_IN = 71
    # LEFT_BOX_BRACKET = 82
    # RIGHT_BOX_BRACKET = 83
    # STRING = 91
    # BREAK = 107
    # WHILE = 113
    # GLOBAL = 114
    # CONTINUE = 109
    # FOR = 110

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