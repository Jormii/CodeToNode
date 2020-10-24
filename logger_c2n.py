import sys


def log_error(filename, line, message):
    sys.exit("Error parsing the file \"{}\" in line {}: {}".format(
        filename, line, message))
