import sys
from enum import Enum, auto


class ErrorStep(Enum):
    SCANNING = auto()
    PARSING = auto()
    RUNTIME = auto()


def log_error(filename, line, step, message):
    sys.exit("Error found in file \"{}\", in line {} during {}: {}".format(
        filename, line, step.name, message))
