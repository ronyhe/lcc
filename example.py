zero = lambda x: (lambda y: (y))
one = lambda x: (lambda y: ((y)(x)))


if __name__ == "__main__":
    one