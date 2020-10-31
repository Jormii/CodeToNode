:
    counter = 2
    number = 5
    prime = True
    while prime and counter != number:
        if number % counter == 0:
            prime = False

        counter = counter + 1

    PRIME = prime
