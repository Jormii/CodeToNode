# CodeToNode
The purpose of CodeToNode is providing a way of programming Blender shaders using Python code instead of the built-in node system

## Motivation
- Blender doesn't support GLSL. The closest to this is OSL, which can only be used in Cycles and whose performance isn't the best.
- Although the node system is comfortable, it can be messy if the system becomes big.

## Steps towards the development
- Programming a simple Python parser that understands a subset of Python's functionality as close as possible to GLSL's systax
- Translating the parsed file to a system of nodes
- Use those nodes to actually build Blender's node tree
- Create addon for Blender

# Current WIP: Building the parser and subset
