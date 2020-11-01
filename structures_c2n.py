class DiffuseBSDF:
    def __init__(self, color, roughness, normal):
        self.color = color
        self.roughness = roughness
        self.normal = normal


class Value:
    def __init__(self, value):
        self.value = value


class RGBA:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Output:
    def __init__(self, surface, volume, displacement):
        self.surface = surface
        self.volume = volume
        self.displacement = displacement


class NodeGroup:
    # TODO
    def __init__(self):
        pass
