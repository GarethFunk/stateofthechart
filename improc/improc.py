import json

import cv2
import numpy as np

if __name__ == '__main__':
    cv2.destroyAllWindows()
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

def convertImageToJSON(filepath):
    ip = cv2.imread(filepath)
    img = cv2.cvtColor(ip, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # increase V to make brighter
    img[:,:,2] = np.multiply(img[:,:,2], 1)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Perform thresholding and binarisation
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    th3 = cv2.erode(th3, kernel, iterations=1)
    th3 = cv2.dilate(th3, kernel, iterations = 1)
    cv2.imshow("Binarised", th3)
    cv2.waitKey(10)
    # Extract shape data
    edges = cv2.Canny(th3, 100, 200)
    cv2.imshow("edges", edges)
    cv2.waitKey(10)
    im2, contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ip, contours, -1, (0, 255, 0), 1)

    # Extract text subimages and process
    # Neglect first hierarchy, go to first child of outer contour
    print(hierarchy)
    outers = []
    pointer =   hierarchy[0, 0, 2]
    while(pointer != -1):
        print(pointer)
        outers.append(contours[pointer])
        pointer = hierarchy[0, pointer, 0]

    # Now we have the bounding contours of all the outer objects.
    # Check the length of each contour to throw out small blobs
    # Check extent of each contour. If it is over say 75% then count it as a rectangle
    # If not it is an arrow
    rect_conts = []
    arrows_conts = []
    for contour in outers:
        if(len(contour) < 50):
            continue
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        rect_area = w * h
        extent = float(area) / rect_area
        if(extent > 0.75):
            rect_conts.append([x, y, w, h])
            cv2.drawContours(ip, contour, -1, (255, 255, 0), 1)
        else:
            # it is an arrow
            arrows_conts.append([x, y, w, h])
            cv2.drawContours(ip, contour, -1, (0, 255, 255), 1)
    # Now we have distinguished between arrows and rectangles
    print(rect_conts)
    print(arrows_conts)
    cv2.imshow("contours", ip)
    cv2.waitKey(1000)
    # Create objects
    nodes = []
    for rect in rect_conts:
        # Extract the text. Assume text is contained within a 90% size bounding rectangle
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        ocr_input = th3[y:y+h, x:x+w]

        nodes.append(Node(Shape.rectangle, (x, y), (w, h), "test"))
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
    op = convertImageToJSON(filepath="../tests/flowchart_images/take2.png")
    print(op)
    cv2.destroyAllWindows()