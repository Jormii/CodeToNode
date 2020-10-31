from scanner_c2n import Scanner
from parser_cn2 import Parser
from interpreter_c2n import Interpreter

from token_c2n import *
from expression_c2n import *
from visitor_c2n import ExpressionPrinter

import sys

branching = "./tests/branching.py"
expression = "./tests/expression.py"
diffuse = "./tests/diffuse.py"

default_file = branching


def print_tokens(tokens):
    print("--- TOKEN INFO ---")

    line = tokens[0].line
    for token in tokens:
        if token.line != line:
            line = token.line
            print()
        print(token)

    print("\n--- CODE ---")
    line = tokens[0].line
    print("{}:\t".format(line), end="")
    indentention = 0
    for token in tokens:
        if token.line != line:
            line = token.line
            print()
            print("{}:\t".format(line), end="")
            print("\t" * indentention, end="")

        if token.token_type == TokenType.LEFT_CURLY_BRACE:
            indentention += 1
        elif token.token_type == TokenType.RIGHT_CURLY_BRACE:
            indentention -= 1
            print()
            print("\t", end="")
            print("\t" * indentention, end="")

        lexeme = token.lexeme
        print(lexeme if lexeme != "" else token.token_type.name, end=" ")
    print()


def scan_tokens(debug=False, filename=default_file):
    file = open(filename, mode="r")
    source_code = file.read()

    scanner = Scanner(filename, source_code)
    tokens = scanner.perform_scanning()

    if debug:
        print_tokens(tokens)
        print("Indentations:", scanner.indentations,
              "-", len(scanner.indentations))

    return tokens


def print_expressions(expressions):
    visitor = ExpressionPrinter()
    for expr in expressions:
        expression_str = expr.accept_visitor(visitor)
        print(expression_str)


def parse_tokens(tokens, filename=default_file, debug=False):
    parser = Parser(filename, tokens)
    expressions = parser.parse()

    if debug:
        print_expressions(expressions)

    return expressions


def interpret_statements(statements, debug=False, filename=default_file):
    interpreter = Interpreter(filename, debug)
    interpreter.interpret(statements)


def main():
    tokens = scan_tokens()
    statements = parse_tokens(tokens)
    interpret_statements(statements, debug=True)


if __name__ == "__main__":
    main()
