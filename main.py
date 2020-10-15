from scanner_c2n import Scanner

from token_c2n import *
from parser_cn2 import *
from expression_c2n import *
from visitor_c2n import ExpressionPrinter

import sys

filename = "./tests/expression.py"

def scan_tokens():
    file = open(filename, mode="r")
    source_code = file.read()

    scanner = Scanner(filename, source_code)
    tokens = scanner.perform_scanning()

    return tokens

def parse_tokens(tokens):
    parser = Parser(tokens)
    expressions = parser.parse()

    return expressions

def main():
    tokens = scan_tokens()
    expressions = parse_tokens(tokens)

    visitor = ExpressionPrinter()
    for expression in expressions:
        expression_string = expression.accept_visitor(visitor)
        print(expression_string)

if __name__ == "__main__":
    main()