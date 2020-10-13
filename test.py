from structures import *

def entry():
    color = (1, 0, 0, 0)
    roughness = 0

    diffuse_mat = DiffuseBSDF(color, roughness, None)

    return diffuse_mat, None, None