import json
import copy

import cv2
import numpy as np
from PIL import Image

if __name__ == '__main__':
    cv2.destroyAllWindows()
    from flowchart.small_classes import Face
    from flowchart.small_classes import Shape
    from flowchart.line import Line
    from flowchart.node import Node
    from flowchart.fcEncoder import fcEncoder
    from ocr import ocr
else:
    from .flowchart.small_classes import Face
    from .flowchart.small_classes import Shape
    from .flowchart.line import Line
    from .flowchart.node import Node
    from .flowchart.fcEncoder import fcEncoder
    from .ocr import ocr

def convertImageToJSON(filepath):
    ip = cv2.imread(filepath)
    static_input = copy.deepcopy(ip)
    img = cv2.cvtColor(ip, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # increase V to make brighter
    img[:,:,2] += 70
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Perform thresholding and binarisation
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    ret3, th3 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    th3 = cv2.erode(th3, kernel, iterations=1)
    th3 = cv2.dilate(th3, kernel, iterations = 1)
    # Extract shape data
    edges = cv2.Canny(th3, 100, 200)
    im2, contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ip, contours, -1, (0, 255, 0), 1)
    # Extract text subimages and process
    # Neglect first hierarchy, go to first child of outer contour
    outers = []
    pointer =   hierarchy[0, 0, 2]
    while(pointer != -1):
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
            M = cv2.moments(contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            arrows_conts.append([x, y, w, h, cx, cy])
            cv2.drawContours(ip, contour, -1, (0, 255, 255), 1)
    # Now we have distinguished between arrows and rectangles
    # Create objects
    nodes = []
    for rect in rect_conts:
        # Extract the text. Assume text is contained within a 90% size bounding rectangle
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        d = 0.150 #indent
        ocr_input = static_input[int(y+(h*d)):int(y+(h*(1-d))), int(x+(d*w)):int(x+(w*(1-d)))]
        kernel = np.ones((3, 3), np.uint8)
        #ocr_input = cv2.cvtColor(ocr_input, cv2.COLOR_BGR2RGB)
        if __name__ == '__main__':
            cv2.imshow("text", ocr_input)
            cv2.waitKey(0)
        ocr_input = Image.fromarray(ocr_input)
        text = ocr(ocr_input)
        if len(text) == 0:
            text = ""
        else:
            text = text[0]
        print(text)
        nodes.append(Node(Shape.rectangle, (x+(w/2), y+(h/2)), (w, h), text))
    lines = []
    for line in arrows_conts:
        x = line[0]
        y = line[1]
        w = line[2]
        h = line[3]
        x += w/2
        y += h/2
        cx = line[4]
        cy = line[5]
        l1_start = []
        l1_end = []
        # Determine start node and end node
        if w > h:
            # The arrow points is horizontal
            length = w
            if cx > x:
                # Arrow head is on the right
                startFace = Face.right
                start = x - (w/2)
                endFace = Face.left
                end = x + (w/2)
                for node in nodes:
                    # Start node must be to the left of start
                    dist = start - node.pos[0] # should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_start.append(dist + abs(y - node.pos[1]))
                    # End node must be to the right of end
                    dist = node.pos[0] - end # should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_end.append(dist + abs(y - node.pos[1]))
            else:
                # Arrow head is on the left
                startFace = Face.left
                start = x + (w/2)
                endFace = Face.right
                end = x - (w/2)
                for node in nodes:
                    # Start node must be to the right of start
                    dist = node.pos[0] - start # should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_start.append(dist + abs(y - node.pos[1]))
                    # End node must be to the left of end
                    dist = end - node.pos[0]# should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_end.append(dist + abs(y - node.pos[1]))
        else:
            # The arrow is vertical
            length = h
            if cy > y:
                # Arrow points down
                startFace = Face.bottom
                start = y - (h/2)
                endFace = Face.top
                end = y + (h/2)
                for node in nodes:
                    # Start node must be above of start
                    dist = start - node.pos[1] # should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_start.append(dist + abs(y - node.pos[0]))
                    # End node must be below end
                    dist = node.pos[1] - end # should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_end.append(dist + abs(y - node.pos[0]))
            else:
                # Arrow points up
                startFace = Face.top
                start = y + (h/2)
                endFace = Face.bottom
                end = y - (h/2)
                for node in nodes:
                    # Start node must be below start
                    dist = node.pos[1] - start# should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_start.append(dist + abs(y - node.pos[1]))
                    # End node must be above of end
                    dist = end - node.pos[1]# should be +ve
                    if dist < 0:
                        dist = 100000000
                    l1_end.append(dist + abs(y - node.pos[1]))
        # Find shortest distances
        startnode = nodes[np.argmin(l1_start)]
        endnode = nodes[np.argmin(l1_end)]
        if(startFace == Face.top or startFace == Face.bottom):
            startpos = x - (startnode.pos[0] - (startnode.size[0]/2))
            endpos = x - (endnode.pos[0] - (endnode.size[0]/2))
            print(str(startnode.size[0]) + " pos: " + str(startpos))
            print(str(endnode.size[0]) + " pos: " + str(endpos))
        else:
            startpos = y - (startnode.pos[1] - (startnode.size[1] / 2))
            endpos = y - (endnode.pos[1] - (endnode.size[1] / 2))
            print(str(startnode.size[1]) + " pos: " + str(startpos))
            print(str(endnode.size[1]) + " pos: " + str(endpos))
        # create line and append
        lines.append(Line(startnode, startFace, endnode, endFace, startpos, endpos))
    # Aggregate objects
    flowchart = { "nodes":nodes, "lines":lines}
    # Convert to JSON
    output = json.dumps(flowchart, cls=fcEncoder)
    if __name__ == '__main__':
        cv2.imshow("Binarised", th3)
        cv2.waitKey(10)
        cv2.imshow("edges", edges)
        cv2.waitKey(10)
        cv2.imshow("contours", ip)
        cv2.waitKey(0)
    return output


if __name__ == '__main__':
    op = convertImageToJSON(filepath="../tests/flowchart_images/newtest.jpg")
    print(op)
    cv2.destroyAllWindows()
    quit()

