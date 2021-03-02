import transpiler.expression_c2n as expr
import transpiler.statement_c2n as stmt
from transpiler.environment_c2n import Environment
from transpiler.token_c2n import Token, TokenType
from transpiler.callable_c2n import Callable, CustomFunction
from transpiler.visitor_c2n import VisitorInterface
from transpiler.exception_c2n import ReturnException
from transpiler.logger_c2n import log_error, ErrorStep


class Interpreter(VisitorInterface):

    def __init__(self, filename, debug=False):
        self.environment = Environment(filename)

        self.filename = filename
        self.debug = debug

        self.initialize_native_functions()

    def initialize_native_functions(self):
        return

    def interpret(self, statements):
        self.check_unsupported_actions(statements)

        for statement in statements:
            self.execute(statement)

        # Ugly, but needed
        virtual_main_token = Token(TokenType.IDENTIFIER, -1, "main")
        main_func = self.environment.get(virtual_main_token)
        if main_func.arity() != 0:
            log_error(self.filename, main_func.declaration.name.line,
                      ErrorStep.RUNTIME, "\"main\" must have no parameters")

        exit_code = main_func.call(self, [])
        print("END OF EXECUTION. Value returned from \"main\":", exit_code)

    def check_unsupported_actions(self, statements):
        self.check_for_single_return(statements)
        self.check_for_recursion(statements)

    def check_for_single_return(self, statements):
        for statement in statements:
            if not isinstance(statement, stmt.Function):
                continue

            body = statement.body
            number_of_returns = 0
            for func_stmt in body:
                number_of_returns += self.count_number_of_returns(func_stmt)

            name = statement.name.lexeme
            line = statement.name.line
            if number_of_returns == 0:
                log_error(self.filename, line, ErrorStep.RUNTIME,
                          "Function \"{}\" returns no values".format(name))
            elif number_of_returns > 1:
                log_error(self.filename, line, ErrorStep.RUNTIME,
                          "Function \"{}\" has more than one return".format(name))

            last_statement = body[-1]
            if not isinstance(last_statement, stmt.Return):
                log_error(self.filename, line, ErrorStep.RUNTIME,
                          "Function \"{}\": The last statement must be a return statement".format(name))

    def count_number_of_returns(self, statement):
        if isinstance(statement, stmt.Block):
            returns = 0
            for stmt_in_block in statement.statements:
                returns += self.count_number_of_returns(stmt_in_block)
            return returns

        if isinstance(statement, stmt.Expression):
            return 0

        if isinstance(statement, stmt.Function):
            line = statement.name.line
            log_error(self.filename, line, ErrorStep.RUNTIME,
                      "Function \"{}\": Local functions aren't supported".format(statement.name.lexeme))

        if isinstance(statement, stmt.If):
            then_returns = self.count_number_of_returns(statement.then_branch)
            else_returns = 0 if statement.else_branch is None else self.count_number_of_returns(
                statement.else_branch)
            return then_returns + else_returns

        if isinstance(statement, stmt.Return):
            return 1

        if isinstance(statement, stmt.Variable):
            return 0

        if isinstance(statement, stmt.While):
            log_error(self.filename, -1, ErrorStep.RUNTIME,
                      "While statements aren't supported")

        log_error(self.filename, -1, ErrorStep.RUNTIME,
                  "Shouldn't reach this point")

    def check_for_recursion(self, statements):
        calls = {}
        for statement in statements:
            if not isinstance(statement, stmt.Function):
                continue

            func_name = statement.name.lexeme
            functions_called_within_func = set()
            self.find_functions_called_in_statements(
                statement.body, functions_called_within_func)

            if func_name in functions_called_within_func:
                log_error(self.filename, statement.name.line,
                          ErrorStep.RUNTIME, "Found direct recursion")

            calls[func_name] = functions_called_within_func

        # TODO: Check for indirect recursion
        for fun in calls.keys():
            self.check_for_indirect_recursion(fun, calls, [])

    def find_functions_called_in_statements(self, statements, set_of_funcs):
        for statement in statements:
            self.find_functions_called_in_statement(statement, set_of_funcs)

    def find_functions_called_in_statement(self, statement, set_of_funcs):
        if isinstance(statement, stmt.Block):
            self.find_functions_called_in_statements(
                statement.statements, set_of_funcs)
        elif isinstance(statement, stmt.Expression):
            self.find_functions_called_in_expression(
                statement.expression, set_of_funcs)
        elif isinstance(statement, stmt.Function):
            log_error(self.filename, statement.name.line,
                      ErrorStep.RUNTIME, "Shouldn't reach this point")
        elif isinstance(statement, stmt.If):
            self.find_functions_called_in_expression(
                statement.condition, set_of_funcs)
            self.find_functions_called_in_statements(
                statement.then_branch.statements, set_of_funcs)
            if statement.else_branch is not None:
                self.find_functions_called_in_statements(
                    statement.else_branch.statements, set_of_funcs)
        elif isinstance(statement, stmt.Return):
            self.find_functions_called_in_expression(
                statement.value, set_of_funcs)
        elif isinstance(statement, stmt.Variable):
            self.find_functions_called_in_expression(
                statement.initializer, set_of_funcs)

    def find_functions_called_in_expression(self, expression, set_of_funcs):
        if isinstance(expression, expr.Assignment):
            self.find_functions_called_in_expression(
                expression.value, set_of_funcs)
        elif isinstance(expression, expr.Binary):
            self.find_functions_called_in_expression(
                expression.left, set_of_funcs)
            self.find_functions_called_in_expression(
                expression.right, set_of_funcs)
        elif isinstance(expression, expr.Call):
            set_of_funcs.add(expression.callee.name.lexeme)
        elif isinstance(expression, expr.Grouping):
            self.find_functions_called_in_expression(
                expression.expression, set_of_funcs)
        elif isinstance(expression, expr.Literal):
            return
        elif isinstance(expression, expr.Logical):
            self.find_functions_called_in_expression(
                expression.left, set_of_funcs)
            self.find_functions_called_in_expression(
                expression.right, set_of_funcs)
        elif isinstance(expression, expr.Unary):
            self.find_functions_called_in_expression(
                expression.right, set_of_funcs)
        elif isinstance(expression, expr.Variable):
            return

    def check_for_indirect_recursion(self, fun, calls, virtual_stack):
        if fun in virtual_stack:
            # Add so it's displayed on the error
            virtual_stack.append(fun)
            log_error(self.filename, -1, ErrorStep.RUNTIME,
                      "Found indirect recursion. Recursion isn't allowed. Stack: {}".format(virtual_stack))

        virtual_stack.append(fun)
        for fun_call in calls[fun]:
            self.check_for_indirect_recursion(fun_call, calls, virtual_stack)

    def execute(self, statement):
        statement.accept_visitor(self)

    def evaluate(self, expression):
        return expression.accept_visitor(self)

    def is_truthy(self, value):
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        return value == 0

    ###
    # VisitorInterface
    ###

    def visit_assigment_expression(self, expression):
        token = expression.token
        value = self.evaluate(expression.expression)

        self.environment.define(token, value)

        if self.debug:
            token = expression.token
            token_str = "{} (line {})".format(token.lexeme, token.line)
            print("{} = {}".format(token_str, value))

        return value

    def visit_binary_expression(self, expression):
        left_value = self.evaluate(expression.left)
        right_value = self.evaluate(expression.right)

        token_type = expression.operator.token_type
        if token_type == TokenType.ADD:
            return left_value + right_value
        if token_type == TokenType.SUBSTRACT:
            return left_value - right_value
        if token_type == TokenType.PRODUCT:
            return left_value * right_value
        if token_type == TokenType.DIVISION:
            return left_value / right_value
        if token_type == TokenType.FLOOR_DIVISION:
            return left_value // right_value
        if token_type == TokenType.MODULUS:
            return left_value % right_value
        if token_type == TokenType.POWER:
            return left_value ** right_value

        if token_type == TokenType.EQUAL:
            return left_value == right_value
        if token_type == TokenType.NOT_EQUAL:
            return left_value != right_value
        if token_type == TokenType.GREATER_THAN:
            return left_value > right_value
        if token_type == TokenType.GREATER_OR_EQUAL:
            return left_value >= right_value
        if token_type == TokenType.LESS_THAN:
            return left_value < right_value
        if token_type == TokenType.LESS_OR_EQUAL:
            return left_value <= right_value

        # Shouldn't reach this point
        log_error(self.filename, expression.token.line, ErrorStep.RUNTIME,
                  "Error while interpreting the file")
        return None

    def visit_call_expression(self, expression):
        line = expression.line
        function = self.evaluate(expression.callee)
        if not isinstance(function, Callable):
            log_error(self.filename, line, ErrorStep.RUNTIME,
                      "Trying to call a not callable instance")

        if self.environment.indentation_level == 0:
            log_error(self.filename, line, ErrorStep.RUNTIME,
                      "Trying to call function \"{}\" from global scope".format(function.declaration.name.lexeme))

        arguments = []
        for arg in expression.arguments:
            arguments.append(self.evaluate(arg))

        if len(arguments) != function.arity():
            log_error(self.filename, line, ErrorStep.RUNTIME,
                      "Expected {} arguments but got {} instead".format(function.arity(), len(arguments)))

        return function.call(self, arguments)

    def visit_get_expression(self, expression):
        obj = self.evaluate(expression.obj)
        x = 0
        # TODO

    def visit_grouping_expression(self, expression):
        return self.evaluate(expression.expression)

    def visit_literal_expression(self, expression):
        return expression.literal

    def visit_logical_expression(self, expression):
        left = self.evaluate(expression.left)
        operator_type = expression.operator.token_type

        if operator_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expression.right)

    def visit_set_expression(self, expression):
        obj = self.evaluate(expression.obj)
        x = 0
        # TODO

    def visit_unary_expression(self, expression):
        value = self.evaluate(expression.right)

        token_type = expression.operator.token_type
        if token_type == TokenType.SUBSTRACT:
            return -value
        if token_type == TokenType.NOT:
            return not self.is_truthy(value)

        # Shouldn't reach this point
        log_error(self.filename, expression.operator.line, ErrorStep.RUNTIME,
                  "Error while interpreting the file")
        return None

    def visit_variable_expression(self, expression):
        token = expression.name
        return self.environment.get(token)

    def visit_block_statement(self, statement):
        self.execute_block(statement.statements)

    def execute_block(self, statements):
        self.environment.new_block()

        for statement in statements:
            self.execute(statement)

        self.environment.end_of_block()

    def visit_expression_statement(self, statement):
        self.evaluate(statement.expression)

    def visit_function_statement(self, statement):
        function = CustomFunction(statement)
        self.environment.define(statement.name, function)

    def visit_if_statement(self, statement):
        condition = statement.condition
        if self.is_truthy(self.evaluate(condition)):
            self.execute(statement.then_branch)
        elif statement.else_branch is not None:
            self.execute(statement.else_branch)

    def visit_return_statement(self, statement):
        value = None

        if statement.value is not None:
            value = self.evaluate(statement.value)

        raise ReturnException(value)

    def visit_variable_statement(self, statement):
        initializer = statement.initializer

        token = statement.name
        value = self.evaluate(initializer)

        self.environment.define(token, value)

        if self.debug:
            token_str = "{} (line {})".format(token.lexeme, token.line)
            print("{} = {}".format(token_str, value))

    def visit_while_statement(self, statement):
        line = statement.condition.operator.line
        log_error(self.filename, line, ErrorStep.RUNTIME,
                  "While loops aren't supported yet")

        condition = statement.condition
        body = statement.body

        while self.is_truthy(self.evaluate(condition)):
            self.execute(body)
