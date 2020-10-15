import sys

class BaseVisitor:

    def visit_literal_expression(self, expression):
        sys.exit("Trying to call BaseVisitor function \"{}\"".format(self.visit_binary_expression.__name__))

    def visit_grouping_expression(self, expression):
        sys.exit("Trying to call BaseVisitor function \"{}\"".format(self.visit_grouping_expression.__name__))

    def visit_unary_expression(self, expression):
        sys.exit("Trying to call BaseVisitor function \"{}\"".format(self.visit_unary_expression.__name__))

    def visit_binary_expression(self, expression):
        sys.exit("Trying to call BaseVisitor function \"{}\"".format(self.visit_binary_expression.__name__))

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
        left_expression_string = expression.left_expression.accept_visitor(self)
        right_expression_string = expression.right_expression.accept_visitor(self)
        return "({} {} {})".format(expression.token.lexeme, left_expression_string, right_expression_string)

class ExpressionVisitor(BaseVisitor):

    def visit_literal_expression(self, expression):
        pass

    def visit_grouping_expression(self, expression):
        pass

    def visit_unary_expression(self, expression):
        pass

    def visit_binary_expression(self, expression):
        pass