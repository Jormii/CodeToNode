class VisitorAccepter:

    def accept_visitor(self, visitor):
        raise NotImplementedError()


class LiteralExpression(VisitorAccepter):

    def __init__(self, literal):
        self.literal = literal

    def accept_visitor(self, visitor):
        return visitor.visit_literal_expression(self)


class CallExpression(VisitorAccepter):

    def __init__(self, callee, right_parenthesis_token, arguments):
        self.callee = callee
        self.right_parenthesis_token = right_parenthesis_token
        self.arguments = arguments

    def accept_visitor(self, visitor):
        return visitor.visit_call_expression(self)


class GroupingExpression(VisitorAccepter):

    def __init__(self, expression):
        self.expression = expression    # Translates to (<expression>)

    def accept_visitor(self, visitor):
        return visitor.visit_grouping_expression(self)


class LogicalExpression(VisitorAccepter):

    def __init__(self, left_expression, token, right_expression):
        self.left_expression = left_expression
        self.token = token
        self.right_expression = right_expression

    def accept_visitor(self, visitor):
        return visitor.visit_logical_expression(self)


class UnaryExpression(VisitorAccepter):

    # <unary operation token><expression>, e.g. -5 or not(a and b)
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_unary_expression(self)


class AssignmentExpression(VisitorAccepter):

    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_assignment_expression(self)


class BinaryExpression(VisitorAccepter):

    # <left_expression><binary operation token><right expression>, e.g. a + b
    def __init__(self, left_expression, token, right_expression):
        self.left_expression = left_expression
        self.token = token
        self.right_expression = right_expression

    def accept_visitor(self, visitor):
        return visitor.visit_binary_expression(self)


class VariableExpression(VisitorAccepter):

    def __init__(self, token):
        self.token = token

    def accept_visitor(self, visitor):
        return visitor.visit_variable_expression(self)


class Block(VisitorAccepter):

    def __init__(self, statements):
        self.statements = statements

    def accept_visitor(self, visitor):
        return visitor.visit_block(self)


class Expression(VisitorAccepter):

    def __init__(self, expression):
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_statement(self)


class Function(VisitorAccepter):

    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept_visitor(self, visitor):
        return visitor.visit_function(self)


class If(VisitorAccepter):

    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept_visitor(self, visitor):
        return visitor.visit_if(self)


class Return(VisitorAccepter):

    def __init__(self, return_token, value):
        self.return_token = return_token
        self.value = value

    def accept_visitor(self, visitor):
        return visitor.visit_return(self)


class Variable(VisitorAccepter):

    # <identifier_token> = <expression>
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_variable_declaration(self)


class While(VisitorAccepter):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept_visitor(self, visitor):
        return visitor.visit_while(self)
