from enum import Enum

class Shape(Enum):
    none = 0
    rectangle = 1
    terminus = 2
    diamond = 3

class Face(Enum):
    none = 0
    top = 1
    right  = 2
    bottom  = 3
    left = 4

class Connector:
    node = -1
    face = Face.none
    pos = -1    # 1D Position along face with origin as top-left-most vertex of edge

    def __init__(self, node, face, pos = -1):
        self.node = node
        self.face = face
        if pos is -1:
            # Calculate the middle of that face
            if (self.face is Face.top or self.face is Face.bottom):
                # Use the width
                self.pos = node.size[0]/2
            elif (self.face is Face.left or self.face is Face.right):
                # Use the height
                self.pos = node.size[1]/2
            else:
                self.pos = -1
        else:
            self.pos  = pos



