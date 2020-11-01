def add(a, b):
    addition = a + b


def count(n):
    if n > 1:
        count(n - 1)

    c = n


def is_even(n):
    if n == 0:
        even = True
    else:
        is_odd(n - 1)


def is_odd(n):
    if n == 0:
        even = False
    else:
        is_even(n - 1)


:
    p = 6

    add(1, 2)
    count(p)
    is_even(p)

    p = p + 0
