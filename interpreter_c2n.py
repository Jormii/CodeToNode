from visitor_c2n import *

class Interpreter:

    def __init__(self, print_statements):
        self.visitor = ExpressionVisitor()

        self.print_statements = print_statements
        self.printer_visitor = ExpressionPrinter()

    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)

            if self.print_statements:
                string = statement.accept_visitor(self.printer_visitor)
                print(string)

    def execute(self, statement):
        statement.accept_visitor(self.visitor)