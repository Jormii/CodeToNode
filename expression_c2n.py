import sys


class VisitorAccepter:

    def accept_visitor(self, visitor):
        raise NotImplementedError()


class LiteralExpression(VisitorAccepter):

    def __init__(self, literal):
        self.literal = literal

    def accept_visitor(self, visitor):
        return visitor.visit_literal_expression(self)


class GroupingExpression(VisitorAccepter):

    def __init__(self, expression):
        self.expression = expression    # Translates to (<expression>)

    def accept_visitor(self, visitor):
        return visitor.visit_grouping_expression(self)


class UnaryExpression(VisitorAccepter):

    # <unary operation token><expression>, e.g. -5 or not(a and b)
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_unary_expression(self)


class BinaryExpression(VisitorAccepter):

    # <left_expression><binary operation token><right expression>, e.g. a + b
    def __init__(self, left_expression, token, right_expression):
        self.left_expression = left_expression
        self.token = token
        self.right_expression = right_expression

    def accept_visitor(self, visitor):
        return visitor.visit_binary_expression(self)


class StatementExpression(VisitorAccepter):

    def __init__(self, expression):
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_statement(self)
