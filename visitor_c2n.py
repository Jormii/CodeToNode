class VisitorInterface:

    # Expressions
    def visit_assigment_expression(self, expression):
        raise NotImplementedError()

    def visit_binary_expression(self, expression):
        raise NotImplementedError()

    def visit_call_expression(self, expression):
        raise NotImplementedError()

    def visit_grouping_expression(self, expression):
        raise NotImplementedError()

    def visit_literal_expression(self, expression):
        raise NotImplementedError()

    def visit_logical_expression(self, expression):
        raise NotImplementedError()

    def visit_unary_expression(self, expression):
        raise NotImplementedError()

    def visit_variable_expression(self, expression):
        raise NotImplementedError()

    # Statements
    def visit_block_statement(self, statement):
        raise NotImplementedError()

    def visit_expression_statement(self, statement):
        raise NotImplementedError()

    def visit_function_statement(self, statement):
        raise NotImplementedError()

    def visit_if_statement(self, statement):
        raise NotImplementedError()

    def visit_return_statement(self, statement):
        raise NotImplementedError()

    def visit_variable_statement(self, statement):
        raise NotImplementedError()

    def visit_while_statement(self, statement):
        raise NotImplementedError()


class VisitorAccepterInterface:

    def accept_visitor(self, visitor):
        raise NotImplementedError()
