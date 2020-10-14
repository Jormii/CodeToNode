from structures import *

class BaseNode:
    material_name: str
    node_id: str

    def __init__(self, material_name: str, node_id: str):
        self.material_name = material_name
        self.node_id = node_id

    def parse_node(self):
        return "bpy.data.materials[\"{}\"].node_tree.nodes[\"{}\"].".format(self.material_name, self.node_id)

class Output_n(BaseNode):
    node_item = "19"

    output: Output

    def __init__(self, material_name: str, node_id: str, output: Output):
        super().__init__(material_name, node_id)
        self.output = output

    def parse_node(self):
        base = super().parse_node()
        surface_line = "{}inputs[0].default_value[0] = {}".format(base, self.output.surface)
        volume_line = "{}inputs[0].default_value[1] = {}".format(base, self.output.volume)
        displacement_line = "{}inputs[0].default_value[2] = {}".format(base, self.output.displacement)
        return [surface_line, volume_line, displacement_line]


class RGBA_n(BaseNode):
    node_item = "11"

    rgba: RGBA

    def __init__(self, material_name: str, node_id: str, rgba: RGBA):
        super().__init__(material_name, node_id)
        self.rgba = rgba

    def parse_node(self):
        base = super().parse_node()
        r_line = "{}outputs[0].default_value[0] = {}".format(base, self.rgba.r)
        g_line = "{}outputs[0].default_value[1] = {}".format(base, self.rgba.g)
        b_line = "{}outputs[0].default_value[2] = {}".format(base, self.rgba.b)
        a_line = "{}outputs[0].default_value[3] = {}".format(base, self.rgba.a)
        return [r_line, g_line, b_line, a_line]