
from .small_classes import Connector

class Line:
    """ This class is used to represent lines connecting lines"""
    startCon = -1
    endCon = -1
    kinkPoints = []
    text = ""

    def __init__(self, startNode, startFace, endNode, endFace, startPos = -1, endPos = -1, kinkPoints = [], text = ""):
        self.startCon = Connector(startNode, startFace, startPos)
        self.endCon = Connector(endNode, endFace, endPos)
        self.kinkPoints = kinkPoints
        self.text = text

