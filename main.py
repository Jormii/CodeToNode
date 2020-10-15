from scanner_c2n import Scanner

from token_c2n import *
from expression_c2n import *
from visitor_c2n import ExpressionPrinter

import sys

def test_tokens():
    filename = "./test.py"
    file = open(filename, mode="r")
    source_code = file.read()

    scanner = Scanner(filename, source_code)
    tokens = scanner.perform_scanning()

    if len(tokens) == 0:
        return

    line = tokens[0].line
    for token in tokens:
        if token.line != line:
            print()
            line = token.line

        print(token)

def test_expression_tree():
    unary_expression = UnaryExpression(
        Token(TokenType.SUBSTRACT, 1, "-"),
        LiteralExpression(
            Token(TokenType.NUMBER, 1, "123", 123)
        )
    )

    product_operator = Token(TokenType.PRODUCT, 1, "*")

    grouping_expression = GroupingExpression(
        BinaryExpression(
            LiteralExpression(
                Token(TokenType.NUMBER, 1, "45.67", 45.67)
            ),
            Token(TokenType.FLOOR_DIVISION, 1, "//"),
            LiteralExpression(
                Token(TokenType.NUMBER, 1, "64", 64)
            )
        )
    )

    full_expression = BinaryExpression(unary_expression, product_operator, grouping_expression)

    visitor = ExpressionPrinter()
    expression_string = full_expression.accept_visitor(visitor)
    print(expression_string)

def main():
    test_expression_tree()

if __name__ == "__main__":
    main()