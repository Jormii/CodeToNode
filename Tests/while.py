def main():
    counter = 2
    number = 49
    prime = True
    while prime and counter != number:
        if number % counter == 0:
            prime = False

        counter = counter + 1

    PRIME = prime
