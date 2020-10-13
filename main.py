import sys
# import bpy

from code_parser import Parser

def create_material(material_name: str):
    mat = bpy.data.materials.new(name = material_name)
    mat.use_nodes = True
    mat.node_tree.nodes.clear()

    return mat

def main():
    number_of_arguments = len(sys.argv)
    
    # TODO: Add to final version
    if 0:
        if number_of_arguments != 2:
            print("Error: Provide a .py file with the shader you want to parse")
            exit(-1)

        filename = sys.argv[1]

    filename = "./test.py"  # TODO: Remove line
    parser = Parser(filename)
    parser.parse_file()

    # material_name = "New Material"
    # mat = create_material(material_name)

if __name__ == "__main__":
    main()