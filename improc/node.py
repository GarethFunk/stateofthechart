import uuid

from small_classes import Shape

class Node:
    """This class is used to describe nodes in the flowchart"""
    shape = Shape.none
    pos = (-1, -1)
    size = (-1, -1)
    text = ""
    uid = -1

    def __init__(self, shape, pos, size, text = ""):
        self.shape = shape
        self.pos = pos
        self.size = size
        self.text = text
        self.uid = uuid.uuid4()

