from visitor_c2n import VisitorAccepterInterface


class Statement(VisitorAccepterInterface):

    def accept_visitor(self, visitor):
        raise NotImplementedError()


class Block(Statement):

    def __init__(self, statements):
        self.statements = statements

    def accept_visitor(self, visitor):
        return visitor.visit_block_statement(self)


class Expression(Statement):

    def __init__(self, expression):
        self.expression = expression

    def accept_visitor(self, visitor):
        return visitor.visit_expression_statement(self)


class Function(Statement):

    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept_visitor(self, visitor):
        return visitor.visit_function_statement(self)


class If(Statement):

    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept_visitor(self, visitor):
        return visitor.visit_if_statement(self)


class Return(Statement):

    def __init__(self, return_token, value):
        self.return_token = return_token
        self.value = value

    def accept_visitor(self, visitor):
        return visitor.visit_return_statement(self)


class Variable(Statement):

    # <identifier_token> = <expression>
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept_visitor(self, visitor):
        return visitor.visit_variable_statement(self)


class While(Statement):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept_visitor(self, visitor):
        return visitor.visit_while_statement(self)
