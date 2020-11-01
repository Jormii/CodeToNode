from visitor_c2n import BaseVisitor
from environment_c2n import Environment
from logger_c2n import log_error
from token_c2n import TokenType
from callable_c2n import *
from exceptions_c2n import ReturnException


class Interpreter(BaseVisitor):

    def __init__(self, filename, debug=False):
        self.environment = Environment(filename)

        self.filename = filename
        self.debug = debug

        self.initialize_native_functions()

    def initialize_native_functions(self):
        self.environment.define("clock", ClockCall())

    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        statement.accept_visitor(self)

    def visit_literal_expression(self, expression):
        return expression.literal

    def visit_call_expression(self, expression):
        line = expression.right_parenthesis_token.line
        function = self.evaluate(expression.callee)
        if not isinstance(function, Callable):
            log_error(self.filename, line,
                      "Trying to call a not callable instance")

        arguments = []
        for arg in expression.arguments:
            arguments.append(self.evaluate(arg))

        if len(arguments) != function.arity():
            log_error(self.filename, line, "Expected {} arguments but got {} instead".format(
                function.arity(), len(arguments)))

        return function.call(self, arguments)

    def visit_grouping_expression(self, expression):
        return self.evaluate(expression.expression)

    def visit_logical_expression(self, expression):
        left = self.evaluate(expression.left_expression)
        operator_type = expression.token.token_type

        if operator_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expression.right_expression)

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

    def visit_block(self, block):
        self.execute_block(block.statements)
        return None

    def execute_block(self, statements):
        self.environment.new_block()

        for statement in statements:
            self.execute(statement)

        self.environment.end_of_block()

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

    def visit_function(self, statement):
        function = CustomFunction(statement)
        self.environment.define(statement.name.lexeme, function)
        return None

    def visit_if(self, if_statement):
        condition = if_statement.condition
        if self.is_truthy(self.evaluate(condition)):
            self.execute(if_statement.then_branch)
        elif if_statement.else_branch is not None:
            self.execute(if_statement.else_branch)

        return None

    def visit_return(self, statement):
        value = None

        if statement.value is not None:
            value = self.evaluate(statement.value)

        raise ReturnException(value)

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

    def visit_while(self, expression):
        condition = expression.condition
        body = expression.body

        while self.is_truthy(self.evaluate(condition)):
            self.execute(body)

        return None
