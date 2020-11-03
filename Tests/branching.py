def main():
    number = 1
    is_odd = not ((number % 2) == 0)
    greater_than_zero = number > 0

    if is_odd and greater_than_zero:
        and_is_true = True
    else:
        and_is_true = False

    return 0
