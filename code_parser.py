class Entity:
    def __init__(self, name, content):
        self.name = name
        self.content = content

class Method:
    def __init__(self, name, starting_line, arguments):
        self.name = name
        self.starting_line = starting_line
        self.ending_line = 0
        self.arguments = arguments

class Parser:
    tokens_to_ignore = ["#", "\n", "from"]

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        
        self.entities = {}
        self.methods = {}

    def parse_file(self):
        self.find_methods()

    def find_methods(self):
        lines = self.file.readlines()
        for line_number in range(len(lines)):
            line = lines[line_number]

            if self.ignore_line(line):
                continue

            # Method checking
            splitted_line = line.split()
            if splitted_line[0] == "def":
                method_name, arguments = self.parse_method_header(line)

                if method_name in self.methods:
                    print("Error while parsing: two methods found with the same name \"{}\"".format(method_name))
                    exit(-2)
                
                self.methods[method_name] = Method(method_name, line_number, arguments)

    def ignore_line(self, line):
        for token in Parser.tokens_to_ignore:
            if line.startswith(token):
                return True

        return False
                
    def parse_method_header(self, splitted_line):
        return splitted_line[1], []