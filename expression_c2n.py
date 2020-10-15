class BaseExpression:

    def accept_visitor(self, visitor):
        pass

class LiteralExpression(BaseExpression):

    def __init__(self, literal):
        self.literal = literal

    def accept_visitor(self, visitor):
        return visitor.visit_literal_expression(self)

class GroupingExpression(BaseExpression):

    def __init__(self, expression):
        self.expression = expression

    def accept_visitor(self, visitor):
        return  visitor.visit_grouping_expression(self)

class UnaryExpression(BaseExpression):

    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_unary_expression(self)

class BinaryExpression(BaseExpression):

    def __init__(self, left_expression, token, right_expression):
        self.left_expression = left_expression
        self.token = token
        self.right_expression = right_expression

    def accept_visitor(self, visitor):
        return visitor.visit_binary_expression(self)