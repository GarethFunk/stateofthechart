import json
import uuid
from .small_classes import *
from .node import Node
from .line import Line

class fcEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {"shape":obj.shape, "pos":{"x":obj.pos[0], "y":obj.pos[1]}, "size":{"w":obj.size[0], "h":obj.size[1]}, "text":obj.text, "UID":obj.uid}
        elif isinstance(obj, Line):
            return {"startCon":obj.startCon, "endCon":obj.endCon, "kinkPoints":obj.kinkPoints, "text":obj.text}
        elif isinstance(obj, Connector):
            return {"node":obj.node.uid, "face":obj.face, "pos":obj.pos}
        elif isinstance(obj, Face):
            return obj.name
        elif isinstance(obj, Shape):
            return obj.name
        elif isinstance(obj, uuid.UUID):
            return obj.hex
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)