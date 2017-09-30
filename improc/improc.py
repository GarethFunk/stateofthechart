import json
if __name__ == '__main__':
    from flowchart.small_classes import Face
    from flowchart.small_classes import Shape
    from flowchart.line import Line
    from flowchart.node import Node
    from flowchart.fcEncoder import fcEncoder
else:
    from .flowchart.small_classes import Face
    from .flowchart.small_classes import Shape
    from .flowchart.line import Line
    from .flowchart.node import Node
    from .flowchart.fcEncoder import fcEncoder

def convertImageToJSON(filepath = ""):
    #input = cv2.imread(filepath)
    # Perform thresholding and binarisation

    # Extract shape data

    # Extract text subimages and process



    # Create objects
    nodes = []
    nodes.append(Node(Shape.terminus, (50, 10), (20, 10), "start"))
    nodes.append(Node(Shape.rectangle, (50,50), (25, 10), "do shit"))
    lines = []
    lines.append(Line(nodes[0], Face.bottom, nodes[1], Face.top, text="YeSsIr"))
    # Aggregate objects
    flowchart = { "nodes":nodes, "lines":lines}
    # Convert to JSON
    output = json.dumps(flowchart, cls=fcEncoder)

    return output


if __name__ == '__main__':
    op = convertImageToJSON(filepath="")
    print(op)
