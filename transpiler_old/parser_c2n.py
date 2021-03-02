import transpiler.statement_c2n as stmt
import transpiler.expression_c2n as expr
from transpiler.token_c2n import TokenType
from transpiler.exception_c2n import ParsingException
from transpiler.logger_c2n import log_error, ErrorStep


class Parser:

    MAX_ARGUMENTS = 255

    def __init__(self, filename, tokens):
        self.filename = filename
        self.tokens = tokens
        self.statements = []
        self.current = 0

    def parse(self):
        while not self.is_at_end():
            statement = self.declaration()
            self.statements.append(statement)

        return self.statements

    def declaration(self):
        try:
            if self.match([TokenType.IDENTIFIER]):
                # Identifiers can be both assignment or function call
                # If it's assignment
                if self.check(TokenType.ASSIGMENT):
                    return self.var_declaration()

                # If it's function call, undo advance produced by self.match. Continue to self.statement below
                self.rollback()
            elif self.match([TokenType.DEF]):
                return self.function()
            elif self.match([TokenType.RETURN]):
                return self.return_statement()

            return self.statement()

        except ParsingException:
            self.synchronize()
            log_error(self.filename, self.previous().line,
                      ErrorStep.PARSING, "Syntax error")

    def var_declaration(self):
        identifier_token = self.previous()
        self.consume(TokenType.ASSIGMENT)

        initializer = self.expression()
        self.consume(TokenType.SEMICOLON)

        declaration = stmt.Variable(identifier_token, initializer)
        return declaration

    def function(self):
        name = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.LEFT_PARENTHESIS)

        parameters = []
        if not self.check(TokenType.RIGHT_PARENTHESIS):
            parameters.append(self.consume(TokenType.IDENTIFIER))
            while self.match([TokenType.COMMA]):
                if len(parameters) >= Parser.MAX_ARGUMENTS:
                    log_error(self.filename, name.line, ErrorStep.PARSING, "Can't have more than {} parameters".format(
                        Parser.MAX_ARGUMENTS))
                parameters.append(self.consume(TokenType.IDENTIFIER))

        self.consume(TokenType.RIGHT_PARENTHESIS)

        self.consume(TokenType.LEFT_CURLY_BRACE)
        body = self.block()
        return stmt.Function(name, parameters, body)

    def return_statement(self):
        return_token = self.previous()

        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON)
        return stmt.Return(return_token, value)

    def statement(self):
        if self.match([TokenType.IF]):
            return self.if_statement()
        elif self.match([TokenType.WHILE]):
            return self.while_statement()
        elif self.match([TokenType.LEFT_CURLY_BRACE]):
            block = self.block()
            return stmt.Block(block)

        return self.expression_statement()

    def if_statement(self):
        condition = self.expression()

        then_branch = self.statement()
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()

        return stmt.If(condition, then_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        body = self.statement()

        return stmt.While(condition, body)

    def block(self):
        statements = []

        while not self.check(TokenType.RIGHT_CURLY_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_CURLY_BRACE)
        return statements

    def expression_statement(self):
        expression = self.expression()
        self.consume(TokenType.SEMICOLON)
        return stmt.Expression(expression)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expression = self.or_expr()

        if self.match([TokenType.ASSIGMENT]):
            assigment_token = self.previous()
            value = self.assignment()

            if isinstance(value, expr.Variable):
                token = value.token
                return expr.Assignment(token, value)
            elif isinstance(expression, expr.Get):
                return expr.Set(expression.obj, expression.name, value)

            log_error(self.filename, assigment_token.line,
                      ErrorStep.PARSING, "Invalid assigment")

        return expression

    def or_expr(self):
        expression = self.and_expr()

        while self.match([TokenType.OR]):
            operator = self.previous()
            right_expression = self.and_expr()
            expression = expr.Logical(
                expression, operator, right_expression)

        return expression

    def and_expr(self):
        expression = self.equality()

        while self.match([TokenType.AND]):
            operator = self.previous()
            right_expression = self.equality()
            expression = expr.Logical(
                expression, operator, right_expression)

        return expression

    def equality(self):
        expression = self.comparison()

        while self.match([TokenType.EQUAL, TokenType.NOT_EQUAL]):
            operator = self.previous()
            right_expression = self.comparison()
            expression = expr.Binary(
                expression, operator, right_expression)

        return expression

    def comparison(self):
        expression = self.term()

        while self.match([TokenType.GREATER_THAN, TokenType.GREATER_OR_EQUAL,
                          TokenType.LESS_THAN, TokenType.LESS_OR_EQUAL]):
            operator = self.previous()
            right_expression = self.term()
            expression = expr.Binary(
                expression, operator, right_expression)

        return expression

    def term(self):
        expression = self.factor()

        while self.match([TokenType.ADD, TokenType.SUBSTRACT]):
            operator = self.previous()
            right_expression = self.factor()
            expression = expr.Binary(
                expression, operator, right_expression)

        return expression

    def factor(self):
        expression = self.power()

        while self.match([TokenType.PRODUCT, TokenType.DIVISION,
                          TokenType.FLOOR_DIVISION, TokenType.MODULUS]):
            operator = self.previous()
            right_expression = self.power()
            expression = expr.Binary(
                expression, operator, right_expression)

        return expression

    def power(self):
        expression = self.unary()

        while self.match([TokenType.POWER]):
            operator = self.previous()
            right_expression = self.unary()
            expression = expr.Binary(
                expression, operator, right_expression)

        return expression

    def unary(self):
        if self.match([TokenType.NOT, TokenType.SUBSTRACT]):
            operator = self.previous()
            right_expression = self.unary()
            return expr.Unary(operator, right_expression)

        return self.call()

    def call(self):
        expression = self.primary()

        while True:
            if self.match([TokenType.LEFT_PARENTHESIS]):
                expression = self.finish_call(expression)
            elif self.match([TokenType.DOT]):
                name = self.consume(TokenType.IDENTIFIER)
                expression = expr.Get(expression, name)
            else:
                break

        return expression

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PARENTHESIS):
            arguments.append(self.expression())
            while self.match([TokenType.COMMA]):
                if len(arguments) >= Parser.MAX_ARGUMENTS:
                    log_error(self.filename, -1, ErrorStep.PARSING,
                              "Can't have more than {} arguments".format(Parser.MAX_ARGUMENTS))

                arguments.append(self.expression())

        line = self.consume(TokenType.RIGHT_PARENTHESIS).line

        return expr.Call(callee, arguments, line)

    def primary(self):
        if self.match([TokenType.TRUE]):
            return expr.Literal(True)
        if self.match([TokenType.FALSE]):
            return expr.Literal(False)
        if self.match([TokenType.NONE]):
            return expr.Literal(None)

        if self.match([TokenType.IDENTIFIER]):
            token = self.previous()
            return expr.Variable(token)
        if self.match([TokenType.NUMBER]):
            literal = self.previous().literal
            return expr.Literal(literal)

        if self.match([TokenType.LEFT_PARENTHESIS]):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PARENTHESIS)
            return expr.Grouping(expression)

        token = self.tokens[self.current]
        raise ParsingException(
            "Expected expression. Last token: {}".format(token))

    def rollback(self):
        self.current -= 1

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def check(self, token_type):
        if self.is_at_end():
            return False

        return self.peek().token_type == token_type

    def match(self, token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type):
        if self.check(token_type):
            return self.advance()

        raise ParsingException(
            "Error parsing: Expecting \"{}\"".format(token_type.name))

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            token = self.peek()
            if token.token_type in [TokenType.DEF, TokenType.RETURN]:
                return

            self.advance()
