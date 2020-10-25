from visitor_c2n import BaseVisitor
from environment_c2n import Environment
from logger_c2n import log_error
from token_c2n import TokenType


class Interpreter(BaseVisitor):

    def __init__(self, filename, debug=False):
        self.environment = Environment(filename)

        self.filename = filename
        self.debug = debug

    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        statement.accept_visitor(self)

    def visit_literal_expression(self, expression):
        return expression.literal

    def visit_grouping_expression(self, expression):
        return self.evaluate(expression.expression)

    def visit_unary_expression(self, expression):
        value = self.evaluate(expression.expression)

        token_type = expression.token.token_type
        if token_type == TokenType.SUBSTRACT:
            return -value
        if token_type == TokenType.NOT:
            return not self.is_truthy(value)

        # Shouldn't reach this point
        log_error(self.filename, expression.token.line,
                  "Error while interpreting the file")

    def visit_assigment_expression(self, expression):
        token = expression.token
        value = self.evaluate(expression.expression)

        self.environment.assign(token, value)

        if self.debug:
            token = expression.token
            token_str = "{} (line {})".format(token.lexeme, token.line)
            print("{} = {}".format(token_str, value))

        return value

    def visit_binary_expression(self, expression):
        left_value = self.evaluate(expression.left_expression)
        right_value = self.evaluate(expression.right_expression)

        token_type = expression.token.token_type
        if token_type == TokenType.ADD:
            return left_value + right_value
        if token_type == TokenType.SUBSTRACT:
            return left_value - right_value
        if token_type == TokenType.PRODUCT:
            return left_value * right_value
        if token_type == TokenType.DIVISION:
            return left_value / right_value
        if token_type == TokenType.FLOOR_DIVISION:
            return left_value // right_value
        if token_type == TokenType.MODULUS:
            return left_value % right_value
        if token_type == TokenType.POWER:
            return left_value ** right_value

        if token_type == TokenType.EQUAL:
            return left_value == right_value
        if token_type == TokenType.NOT_EQUAL:
            return left_value != right_value
        if token_type == TokenType.GREATER_THAN:
            return left_value > right_value
        if token_type == TokenType.GREATER_OR_EQUAL:
            return left_value >= right_value
        if token_type == TokenType.LESS_THAN:
            return left_value < right_value
        if token_type == TokenType.LESS_OR_EQUAL:
            return left_value <= right_value

        # Shouldn't reach this point
        log_error(self.filename, expression.token.line,
                  "Error while interpreting the file")

    def visit_variable_expression(self, expression):
        token = expression.token
        return self.environment.get(token)

    def visit_statement(self, statement):
        self.evaluate(statement.expression)
        return None

    def evaluate(self, expression):
        return expression.accept_visitor(self)

    def is_truthy(self, value):
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return value == 0

    def visit_variable_declaration(self, expression):
        initializer = expression.expression

        name = expression.token.lexeme
        value = self.evaluate(initializer)

        self.environment.define(name, value)

        if self.debug:
            token = expression.token
            token_str = "{} (line {})".format(token.lexeme, token.line)
            print("{} = {}".format(token_str, value))

        return None
