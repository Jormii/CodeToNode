def add(a, b):
    addition = a + b
    return addition


def count(n):
    if n > 1:
        count(n - 1)

    c = n
    return c


def is_even(n):
    return n % 2 == 0


def is_odd(n):
    return not is_even(n)


def fib(n):
    return 0


:
    p = 6

    f = fib(6)

    add(1, 2)
    count(p)
    is_even(p)

    p = p + 0
