from scanner_c2n import Scanner
from parser_cn2 import Parser
from interpreter_c2n import Interpreter
from token_c2n import TokenType

branching = "./Tests/branching.py"
expression = "./Tests/expression.py"
diffuse = "./Tests/diffuse.py"  # Its purpose is checking token scanning
function = "./Tests/function.py"
while_test = "./Tests/while.py"

default_file = while_test


def print_tokens(tokens):
    print("--- TOKEN INFO ---")

    line = tokens[0].line
    for token in tokens:
        if token.line != line:
            line = token.line
            print()
        print(token)

    print("\n--- CODE ---")
    line = tokens[0].line
    print("{}:\t".format(line), end="")
    indentention = 0
    for token in tokens:
        if token.line != line:
            line = token.line
            print()
            print("{}:\t".format(line), end="")
            print("\t" * indentention, end="")

        if token.token_type == TokenType.LEFT_CURLY_BRACE:
            indentention += 1
        elif token.token_type == TokenType.RIGHT_CURLY_BRACE:
            indentention -= 1
            print()
            print("\t", end="")
            print("\t" * indentention, end="")

        lexeme = token.lexeme
        print(lexeme if lexeme != "" else token.token_type.name, end=" ")
    print()


def scan_tokens(debug=False, filename=default_file):
    file = open(filename, mode="r")
    source_code = file.read()

    scanner = Scanner(filename, source_code)
    tokens = scanner.perform_scanning()

    if debug:
        print_tokens(tokens)
        print("Indentations:", scanner.indentations,
              "-", len(scanner.indentations))

    return tokens


def parse_tokens(tokens, filename=default_file):
    parser = Parser(filename, tokens)
    statements = parser.parse()

    return statements


def interpret_statements(statements, debug=False, filename=default_file):
    interpreter = Interpreter(filename, debug)
    interpreter.interpret(statements)


def main():
    tokens = scan_tokens()
    statements = parse_tokens(tokens)
    interpret_statements(statements, debug=True)


if __name__ == "__main__":
    main()
