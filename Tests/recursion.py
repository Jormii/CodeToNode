def a():
    value = 0
    if b():
        value = c()

    return value


def b():
    return c()


def c():
    value = 0
    if b():
        value = a() + d()
    else:
        value = 9

    return b() + value


def d():
    return 0


def main():
    return 0
