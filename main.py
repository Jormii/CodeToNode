from scanner_c2n import Scanner
from parser_cn2 import Parser
from interpreter_c2n import Interpreter

from token_c2n import *
from expression_c2n import *
from visitor_c2n import ExpressionVisitor

import sys

expression = "./tests/expression.py"
diffuse = "./tests/diffuse.py"


def print_tokens(tokens):
    line = tokens[0].line
    for token in tokens:
        if token.line != line:
            line = token.line
            print()
        print(token)


def scan_tokens(debug=False, filename=expression):
    file = open(filename, mode="r")
    source_code = file.read()

    scanner = Scanner(filename, source_code)
    tokens = scanner.perform_scanning()

    if debug:
        print_tokens(tokens)

    return tokens


def parse_tokens(tokens):
    parser = Parser(tokens)
    expressions = parser.parse()

    return expressions


def interpret_statements(statements, print_statements=True):
    interpreter = Interpreter(print_statements)
    interpreter.interpret(statements)


def main():
    tokens = scan_tokens()
    statements = parse_tokens(tokens)
    interpret_statements(statements)


if __name__ == "__main__":
    main()
