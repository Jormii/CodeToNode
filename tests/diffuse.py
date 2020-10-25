from structures_c2n import *


def main():
    color = (1, 2, 3, 4)
    roughness = 5

    def m(a, b, c, d):
        return

    l = 0   # A comment with code before it

    # A comment with no code before it

    diffuse_mat = DiffuseBSDF(color, roughness, None)

    return diffuse_mat, None, None


def other(x):
    if x == 0:
        a = 3
    else:
        a = 5
