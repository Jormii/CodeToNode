from token_c2n import TokenType


class BaseVisitor:

    def visit_literal_expression(self, expression):
        raise NotImplementedError()

    def visit_grouping_expression(self, expression):
        raise NotImplementedError()

    def visit_logical_expression(self, expression):
        raise NotImplementedError()

    def visit_unary_expression(self, expression):
        raise NotImplementedError()

    def visit_assigment_expression(self, expression):
        raise NotImplementedError()

    def visit_binary_expression(self, expression):
        raise NotImplementedError()

    def visit_variable_expression(self, expression):
        raise NotImplementedError()

    def visit_block(self, block):
        raise NotImplementedError()

    def visit_statement(self, statement):
        raise NotImplementedError()

    def visit_if(self, if_statement):
        raise NotImplementedError()

    def visit_variable_declaration(self, expression):
        raise NotImplementedError()


class ExpressionPrinter(BaseVisitor):

    def visit_literal_expression(self, expression):
        return "{}".format(expression.literal)

    def visit_grouping_expression(self, expression):
        expression_string = expression.expression.accept_visitor(self)
        return "group({})".format(expression_string)

    def visit_logical_expression(self, expression):
        left_expression_string = expression.left_expression.accept_visitor(
            self)
        token = expression.token
        right_expression_string = expression.right_expression.accept_visitor(
            self)

        return "({} {} {})".format(left_expression_string, token.lexeme, right_expression_string)

    def visit_unary_expression(self, expression):
        expression_string = expression.expression.accept_visitor(self)
        return "({} {})".format(expression.token.lexeme, expression_string)

    def visit_assigment_expression(self, expression):
        token = expression.token
        assigment = expression.expression

        return "{} = {}".format(token.lexeme, assigment.accept_visitor(self))

    def visit_binary_expression(self, expression):
        left_expression_string = expression.left_expression.accept_visitor(
            self)
        right_expression_string = expression.right_expression.accept_visitor(
            self)
        return "({} {} {})".format(expression.token.lexeme, left_expression_string, right_expression_string)

    def visit_variable_expression(self, expression):
        token = expression.token
        return "{}".format(token.lexeme)

    def visit_block(self, block):
        statements = block.statements
        for statement in statements:
            statement.accept_visitor(self)

    def visit_statement(self, statement):
        statement_string = statement.expression.accept_visitor(self)
        return "{}".format(statement_string)

    def visit_if(self, if_statement):
        condition_string = if_statement.condition.accept_visitor(self)
        then_string = if_statement.then_branch.accept_visitor(self)
        else_string = "" if if_statement.else_branch is None else if_statement.else_branch.accept_visitor(
            self)

        string = "if ({})".format(condition_string)
        string += "\n{\n"
        string += then_string
        string += "\n}"

        if else_string == "":
            return string

        string += "\n{\n"
        string += else_string
        string += "\n}"
        return string

    def visit_variable_declaration(self, expression):
        token = expression.token
        declaration = expression.expression

        declaration_str = declaration.accept_visitor(self)
        return "{} = {}".format(token.lexeme, declaration_str)
