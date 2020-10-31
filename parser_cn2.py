from token_c2n import *
from expression_c2n import *
from logger_c2n import log_error

import sys


class Parser:

    def __init__(self, filename, tokens):
        self.filename = filename
        self.tokens = tokens
        self.statements = []
        self.current = 0

    def parse(self):
        while not self.is_at_end():
            statement = self.declaration()
            self.statements.append(statement)

        return self.statements

    def declaration(self):
        try:
            if self.match([TokenType.IDENTIFIER]):
                return self.var_declaration()

            return self.statement()
        except Exception as e:
            self.synchronize()
            log_error(self.filename, self.previous().line, "Syntax error")

    def var_declaration(self):
        identifier_token = self.previous()
        self.consume(TokenType.ASSIGMENT)

        initializer = self.expression()
        self.consume(TokenType.SEMICOLON)

        declaration = Variable(identifier_token, initializer)
        return declaration

    def statement(self):
        if self.match([TokenType.IF]):
            return self.if_statement()
        elif self.match([TokenType.WHILE]):
            return self.while_statement()
        elif self.match([TokenType.LEFT_CURLY_BRACE]):
            block = self.block()
            return Block(block)

        return self.expression_statement()

    def if_statement(self):
        condition = self.expression()

        then_branch = self.statement()
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        body = self.statement()

        return While(condition, body)

    def block(self):
        statements = []

        while not self.check(TokenType.RIGHT_CURLY_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_CURLY_BRACE)
        return statements

    def expression_statement(self):
        expression = self.expression()
        self.consume(TokenType.SEMICOLON)
        return Expression(expression)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expression = self.or_expr()

        if self.match([TokenType.ASSIGMENT]):
            assigment_token = self.previous()
            value = self.assignment()

            if value is VariableExpression:
                token = value.token
                return AssignmentExpression(token, value)

            log_error(self.filename, assigment_token.line, "Invalid assigment")

        return expression

    def or_expr(self):
        expression = self.and_expr()

        while self.match([TokenType.OR]):
            operator = self.previous()
            right_expression = self.and_expr()
            expression = LogicalExpression(
                expression, operator, right_expression)

        return expression

    def and_expr(self):
        expression = self.equality()

        while self.match([TokenType.AND]):
            operator = self.previous()
            right_expression = self.equality()
            expression = LogicalExpression(
                expression, operator, right_expression)

        return expression

    def equality(self):
        expression = self.comparison()

        while self.match([TokenType.EQUAL, TokenType.NOT_EQUAL]):
            operator = self.previous()
            right_expression = self.comparison()
            expression = BinaryExpression(
                expression, operator, right_expression)

        return expression

    def comparison(self):
        expression = self.term()

        while self.match([TokenType.GREATER_THAN, TokenType.GREATER_OR_EQUAL,
                          TokenType.LESS_THAN, TokenType.LESS_OR_EQUAL]):
            operator = self.previous()
            right_expression = self.term()
            expression = BinaryExpression(
                expression, operator, right_expression)

        return expression

    def term(self):
        expression = self.factor()

        while self.match([TokenType.ADD, TokenType.SUBSTRACT]):
            operator = self.previous()
            right_expression = self.factor()
            expression = BinaryExpression(
                expression, operator, right_expression)

        return expression

    def factor(self):
        expression = self.power()

        while self.match([TokenType.PRODUCT, TokenType.DIVISION,
                          TokenType.FLOOR_DIVISION, TokenType.MODULUS]):
            operator = self.previous()
            right_expression = self.power()
            expression = BinaryExpression(
                expression, operator, right_expression)

        return expression

    def power(self):
        expression = self.unary()

        while self.match([TokenType.POWER]):
            operator = self.previous()
            right_expression = self.unary()
            expression = BinaryExpression(
                expression, operator, right_expression)

        return expression

    def unary(self):
        if self.match([TokenType.NOT, TokenType.SUBSTRACT]):
            operator = self.previous()
            right_expression = self.unary()
            return UnaryExpression(operator, right_expression)

        return self.primary()

    def primary(self):
        if self.match([TokenType.TRUE]):
            return LiteralExpression(True)
        if self.match([TokenType.FALSE]):
            return LiteralExpression(False)
        if self.match([TokenType.NONE]):
            return LiteralExpression(None)

        if self.match([TokenType.IDENTIFIER]):
            token = self.previous()
            return VariableExpression(token)
        if self.match([TokenType.NUMBER]):
            literal = self.previous().literal
            return LiteralExpression(literal)

        if self.match([TokenType.LEFT_PARENTHESIS]):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PARENTHESIS)
            return GroupingExpression(expression)

        token = self.tokens[self.current]
        raise Exception("Expected expression. Last token: {}".format(token))

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def check(self, token_type):
        if self.is_at_end():
            return False

        return self.peek().token_type == token_type

    def match(self, token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type):
        if self.check(token_type):
            return self.advance()

        raise Exception(
            "Error parsing: Expecting \"{}\"".format(token_type.name))

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            token = self.peek()
            if token.token_type in [TokenType.DEF, TokenType.RETURN]:
                return

            self.advance()
