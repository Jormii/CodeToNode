from environment_c2n import Environment
from token_c2n import TokenType
from callable_c2n import Callable, CustomFunction
from visitor_c2n import VisitorInterface
from exception_c2n import ReturnException
from logger_c2n import log_error, ErrorStep


class Interpreter(VisitorInterface):

    def __init__(self, filename, debug=False):
        self.environment = Environment(filename)

        self.filename = filename
        self.debug = debug

        self.initialize_native_functions()

    def initialize_native_functions(self):
        return

    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        statement.accept_visitor(self)

    def evaluate(self, expression):
        return expression.accept_visitor(self)

    def is_truthy(self, value):
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return value == 0

    ###
    # VisitorInterface
    ###

    def visit_assigment_expression(self, expression):
        token = expression.token
        value = self.evaluate(expression.expression)

        self.environment.define(token, value)

        if self.debug:
            token = expression.token
            token_str = "{} (line {})".format(token.lexeme, token.line)
            print("{} = {}".format(token_str, value))

        return value

    def visit_binary_expression(self, expression):
        left_value = self.evaluate(expression.left)
        right_value = self.evaluate(expression.right)

        token_type = expression.operator.token_type
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
        log_error(self.filename, expression.token.line, ErrorStep.RUNTIME,
                  "Error while interpreting the file")
        return None

    def visit_call_expression(self, expression):
        line = expression.line
        function = self.evaluate(expression.callee)
        if not isinstance(function, Callable):
            log_error(self.filename, line, ErrorStep.RUNTIME,
                      "Trying to call a not callable instance")

        arguments = []
        for arg in expression.arguments:
            arguments.append(self.evaluate(arg))

        if len(arguments) != function.arity():
            log_error(self.filename, line, ErrorStep.RUNTIME,
                      "Expected {} arguments but got {} instead".format(function.arity(), len(arguments)))

        return function.call(self, arguments)

    def visit_grouping_expression(self, expression):
        return self.evaluate(expression.expression)

    def visit_literal_expression(self, expression):
        return expression.literal

    def visit_logical_expression(self, expression):
        left = self.evaluate(expression.left)
        operator_type = expression.operator.token_type

        if operator_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expression.right)

    def visit_unary_expression(self, expression):
        value = self.evaluate(expression.right)

        token_type = expression.operator.token_type
        if token_type == TokenType.SUBSTRACT:
            return -value
        if token_type == TokenType.NOT:
            return not self.is_truthy(value)

        # Shouldn't reach this point
        log_error(self.filename, expression.operator.line, ErrorStep.RUNTIME,
                  "Error while interpreting the file")
        return None

    def visit_variable_expression(self, expression):
        token = expression.name
        return self.environment.get(token)

    def visit_block_statement(self, statement):
        self.execute_block(statement.statements)

    def execute_block(self, statements):
        self.environment.new_block()

        for statement in statements:
            self.execute(statement)

        self.environment.end_of_block()

    def visit_expression_statement(self, statement):
        self.evaluate(statement.expression)

    def visit_function_statement(self, statement):
        function = CustomFunction(statement)
        self.environment.define(statement.name, function)

    def visit_if_statement(self, statement):
        condition = statement.condition
        if self.is_truthy(self.evaluate(condition)):
            self.execute(statement.then_branch)
        elif statement.else_branch is not None:
            self.execute(statement.else_branch)

    def visit_return_statement(self, statement):
        value = None

        if statement.value is not None:
            value = self.evaluate(statement.value)

        raise ReturnException(value)

    def visit_variable_statement(self, statement):
        initializer = statement.initializer

        token = statement.name
        value = self.evaluate(initializer)

        self.environment.define(token, value)

        if self.debug:
            token_str = "{} (line {})".format(token.lexeme, token.line)
            print("{} = {}".format(token_str, value))

    def visit_while_statement(self, statement):
        condition = statement.condition
        body = statement.body

        while self.is_truthy(self.evaluate(condition)):
            self.execute(body)
