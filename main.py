from scanner_c2n import Scanner

import sys

def main():
    sys.path.append("./")

    filename = "./test.py"
    file = open(filename, mode="r")
    source_code = file.read()

    scanner = Scanner(filename, source_code)
    tokens = scanner.perform_scanning()

    if len(tokens) == 0:
        return

    line = tokens[0].line
    for token in tokens:
        if token.line != line:
            print()
            line = token.line

        print(token)

if __name__ == "__main__":
    main()