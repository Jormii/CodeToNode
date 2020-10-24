from token_c2n import TokenType


class BaseVisitor:

    def visit_literal_expression(self, expression):
        raise NotImplementedError()

    def visit_grouping_expression(self, expression):
        raise NotImplementedError()

    def visit_unary_expression(self, expression):
        raise NotImplementedError()

    def visit_binary_expression(self, expression):
        raise NotImplementedError()

    def visit_statement(self, statement):
        raise NotImplementedError()


class ExpressionPrinter(BaseVisitor):

    def visit_literal_expression(self, expression):
        return "{}".format(expression.literal)

    def visit_grouping_expression(self, expression):
        expression_string = expression.expression.accept_visitor(self)
        return "group({})".format(expression_string)

    def visit_unary_expression(self, expression):
        expression_string = expression.expression.accept_visitor(self)
        return "({} {})".format(expression.token.lexeme, expression_string)

    def visit_binary_expression(self, expression):
        left_expression_string = expression.left_expression.accept_visitor(
            self)
        right_expression_string = expression.right_expression.accept_visitor(
            self)
        return "({} {} {})".format(expression.token.lexeme, left_expression_string, right_expression_string)

    def visit_statement(self, statement):
        statement_string = statement.expression.accept_visitor(self)
        result = statement.expression.accept_visitor(ExpressionVisitor())
        return "{} => {}".format(statement_string, result)


class ExpressionVisitor(BaseVisitor):

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
        return None

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
        return None

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
