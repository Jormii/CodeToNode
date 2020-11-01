from visitor_c2n import VisitorAccepterInterface


class Expression(VisitorAccepterInterface):

    def accept_visitor(self, visitor):
        raise NotImplementedError()


class Assignment(Expression):

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def accept_visitor(self, visitor):
        return visitor.visit_assignment_expression(self)


class Binary(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept_visitor(self, visitor):
        return visitor.visit_binary_expression(self)


class Call(Expression):

    def __init__(self, callee, arguments, line):
        self.callee = callee
        self.arguments = arguments
        self.line = line

    def accept_visitor(self, visitor):
        return visitor.visit_call_expression(self)


class Grouping(Expression):

    def __init__(self, expression):
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_grouping_expression(self)


class Literal(Expression):

    def __init__(self, literal):
        self.literal = literal

    def accept_visitor(self, visitor):
        return visitor.visit_literal_expression(self)


class Logical(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept_visitor(self, visitor):
        return visitor.visit_logical_expression(self)


class Unary(Expression):

    # <unary operation token><expression>, e.g. -5 or not(a and b)
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept_visitor(self, visitor):
        return visitor.visit_unary_expression(self)


class Variable(Expression):

    def __init__(self, name):
        self.name = name

    def accept_visitor(self, visitor):
        return visitor.visit_variable_expression(self)
