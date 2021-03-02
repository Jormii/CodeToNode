import ast

import code_to_node.constants_c2n as constants
from code_to_node.error_logging import log_and_exit


def parse_python_shader(filename):
    python_file = open(filename)
    content = python_file.read()
    expression_tree = ast.parse(content)

    _check_expression_tree(expression_tree)
    return expression_tree

# TODO
# Requirements:
# - Functions must have one return statement
# - Functions can't be recursive, directly or indirectly


def _check_import_from(expression, variables):
    # TODO
    # TODO: How to define custom imports?
    pass


def _check_function_definition(expression, variables):
    # Check for possible redefinition
    if expression.name in variables.all_funcs:
        error_text = "Error in function {} defined in line {}: This function was already defined".format(
            expression.name, expression.lineno)
        log_and_exit(error_text)

    # Functions within functions aren't allowed
    if variables.current_func is not None:
        error_text = "Error in function {} defined in line {}: Functions within functions aren't allowed".format(
            expression.name, expression.lineno)
        log_and_exit(error_text)

    variables.all_funcs.add(expression.name)
    variables.current_func = expression.name
    variables.func_calls[variables.current_func] = []
    variables.func_returns[variables.current_func] = []

    # Main can't have arguments
    if expression.name == constants.MAIN_FUNC_NAME:
        arg_length = len(expression.args.args)
        if arg_length > 0:
            error_text = "Main function defined in line {} must have no arguments".format(
                expression.lineno)
            log_and_exit(error_text)

    # Check body of function
    for func_expression in expression.body:
        _call_proper_function(func_expression, variables)

    # Check returns
    returns = variables.func_returns[variables.current_func]
    if len(returns) != 1:
        error_text = "Function {} defined in line {} has 0 or multiple returns".format(
            expression.name, expression.lineno)
        log_and_exit(error_text)

    return_line = returns[0]
    if return_line != expression.end_lineno:
        error_text = "Function {} defined in line {} doesn't return at the end of the function".format(
            expression.name, expression.lineno)
        log_and_exit(error_text)

    variables.current_func = None


def _check_call(expression, variables):
    args = expression.args
    for arg in args:
        _call_proper_function(arg, variables)

    func = expression.func
    variables.func_calls[variables.current_func].append(func.id)


def _check_return(expression, variables):
    variables.func_returns[variables.current_func].append(expression.lineno)
    _call_proper_function(expression.value, variables)


def _check_expr(expression, variables):
    if variables.current_func is None:
        error_text = "Line {}. Expressions aren't allowed outside of functions".format(
            expression.lineno)
        log_and_exit(error_text)

    a = 0


def _check_assign(expression, variables):
    # Can't have multiple targets
    targets = expression.targets
    if len(targets) > 1:
        error_text = "wrong assignment in line {}. Can't assign multiple values at once".format(
            expression.lineno)
        log_and_exit(error_text)

    _call_proper_function(targets[0], variables)

    value = expression.value
    _call_proper_function(value, variables)


def _check_if(expression, variables):
    test = expression.test
    _call_proper_function(test, variables)

    body = expression.body
    for body_expression in body:
        _call_proper_function(body_expression, variables)

    orelse = expression.orelse
    for orelse_expression in orelse:
        _call_proper_function(orelse_expression, variables)


def _check_compare(expression, variables):
    left = expression.left
    _call_proper_function(left, variables)

    comparators = expression.comparators
    for comparator in comparators:
        _call_proper_function(comparator, variables)


def _check_constant(expression, variables):
    # TODO: Lists and such?
    pass


def _check_name(expression, variables):
    pass


CHECKING_FUNCS = {
    # Header
    ast.ImportFrom: _check_import_from,

    # Functions
    ast.FunctionDef: _check_function_definition,
    ast.Call: _check_call,
    ast.Return: _check_return,

    # Expressions
    ast.Expr: _check_expr,
    ast.Assign: _check_assign,
    ast.If: _check_if,

    # Operations
    ast.Compare: _check_compare,

    # Values
    ast.Constant: _check_constant,
    ast.Name: _check_name
}


class CheckingVariables:

    def __init__(self):
        self.all_funcs = set()
        self.current_func = None
        self.func_calls = {}
        self.func_returns = {}


def _check_expression_tree(expression_tree):
    if not isinstance(expression_tree, ast.Module):
        log_and_exit("Python file must be a module on its own")

    variables = CheckingVariables()
    for expression in expression_tree.body:
        _call_proper_function(expression, variables)

    # Check if main function exists
    if constants.MAIN_FUNC_NAME not in variables.all_funcs:
        error_text = "No {} function found in shader".format(
            constants.MAIN_FUNC_NAME)
        log_and_exit(error_text)


def _call_proper_function(expression, variables):
    expr_type = type(expression)
    func = CHECKING_FUNCS[expr_type]
    func(expression, variables)
