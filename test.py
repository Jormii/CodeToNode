from structures_c2n import *

def main():
    color = (1, 2, 3, 4)
    roughness = 5

    l = 0   # AS
    # SA

    diffuse_mat = DiffuseBSDF(color, roughness, None)

    return diffuse_mat, None, None

def m(a, b, c, d):
    return