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

    def visit_variable_expression(self, expression):
        raise NotImplementedError()

    def visit_statement(self, statement):
        raise NotImplementedError()

    def visit_variable_declaration(self, expression):
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

    def visit_variable_expression(self, expression):
        token = expression.token
        return "{} = TODO".format(token.lexeme)

    def visit_statement(self, statement):
        statement_string = statement.expression.accept_visitor(self)
        result = statement.expression.accept_visitor(ExpressionVisitor())
        return "{} => {}".format(statement_string, result)

    def visit_variable_declaration(self, expression):
        token = expression.token
        declaration = expression.expression

        declaration_str = declaration.accept_visitor(self)
        return "{} = {}".format(token.lexeme, declaration_str)
