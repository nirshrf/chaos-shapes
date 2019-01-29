import random
import cv2
import numpy
import time
import math

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
color_list = [red, green, blue]
colors = {}
"""""""""""
def generatePoint(x):
    radius = 300
    angle = (2 * math.pi / x)
    start_point = (radius, radius)
    return_list = []
    for index in range(0, x):
        print angle * 180 / math.pi * index
        x1 = int(start_point[0] + (radius * math.cos(angle * index)))
        y1 = int(start_point[1] + (radius * math.sin(angle * index)))
        point1 = (x1, y1)
        print point1

        #x2 = int(start_point[0] + (radius * math.cos(math.pi - angle * index)))
        #y2 = int(start_point[1] + (radius * math.sin(math.pi - angle * index)))
        #point2 = (x2, y2)
        #print point2

        return_list.append(point1)

    return return_list


"""



def generatePoint(x):
    retList = []
    degree = (2*math.pi/x)
    shift = [300, 300] #[700, 700] #[600, 600]
    radius = 300
    startPoint = [radius, 0]
    for i in range(x):
        tempDegree = degree * i
        rotMat = [[math.cos(tempDegree), -math.sin(tempDegree)], [math.sin(tempDegree), math.cos(tempDegree)]]
        currentPoint = numpy.dot(startPoint, rotMat)
        currentPoint = currentPoint + shift
        if i < 3:
            colors[tuple(currentPoint)] = color_list[i]
        else:
            colors[tuple(currentPoint)] = [random.randint(254, 255), random.randint(0, 255), random.randint(0, 255)]
        retList.append(tuple(currentPoint))
    return retList


def createShape(x):
    blank_image = numpy.zeros((600, 600, 3), numpy.uint8)
    shapeList = generatePoint(x)
    shapeList = [(int(shapeList[i][y])) for i in range(len(shapeList)) for y in range(2)]
    shapeList = zip(shapeList[::2], shapeList[1::2])
    for i in range(x):
        cv2.circle(blank_image, shapeList[i], 2, [255, 0, 0], 1)
        cv2.putText(blank_image, str(i+1), shapeList[i], cv2.FONT_ITALIC, color=[0, 255, 0], thickness=1, fontScale=1)
    return blank_image, shapeList


def nearestColor(currentPoint):
    smallestLen = 10000
    smallPoint = None
    dist_list = []
    for point in colors.keys():
        dist_list.append(dist(currentPoint, point))
    sorted_dist_list = sorted(dist_list)
    color = colors[colors.keys()[dist_list.index(sorted_dist_list[0])]]
    return color


def dist(p1, p2):
    return abs(math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2)))


def createNextPoint(p1, p2, div):
    divisor = div
    shiftX =  0 #800
    shiftY =  0 #800

    nextPoint = ((p1[0] + int((p2[0]-p1[0])/divisor) + shiftX, ((p1[1] + int((p2[1]-p1[1])/divisor)) + shiftY)))
    return nextPoint

def choosePoint(shapeList):
    return random.choice(shapeList)

def chooseFernPoint(trigList):
    x = random.randint(1,10)
    if (x < 3):
        ret = random.choice(trigList[0])
    else:
        ret = random.choice(trigList[1])
    return ret

def generateChaoticShape(x, div):
    iterations = 5000
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    startingPoint = (random.randint(0, 600), random.randint(0, 600))
    myShape, shapeList = createShape(x)
    cv2.imshow('frame', myShape)
    currentPoint = createNextPoint(startingPoint, choosePoint(shapeList), div)
    for prints in range(iterations):
        cv2.putText(myShape, "Number of corners:" + str(x), (50, 50), 3, 1, [0, 0, 255], 2)
        for j in range(iterations/2):
            cv2.circle(myShape, currentPoint, 1, [255,255,255] , 1) #nearestColor(currentPoint)
            currentPoint = createNextPoint(currentPoint, choosePoint(shapeList), div)
        cv2.imshow('frame', myShape)
        if cv2.waitKey(1) == ord("q"):
            break
    return 0

def randTrig():
    blank_image = numpy.zeros((600, 600, 3), numpy.uint8)
    return blank_image, [generatePoint(3), generatePoint(3)]

def coolFern(x):
    iterations = 5000
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    startingPoint = (random.randint(0, 600), random.randint(0, 600))
    myShape, shapeList = randTrig()
    cv2.imshow('frame', myShape)
    currentPoint = createNextPoint(startingPoint, chooseFernPoint(shapeList))
    for prints in range(iterations):
        cv2.putText(myShape, "Number of corners:" + str(x), (50, 50), 3, 1, [0, 0, 255], 2)
        for j in range(iterations/2):
            cv2.circle(myShape, currentPoint, 1, [255, 255, 255], 1) #nearestColor(currentPoint)
            currentPoint = createNextPoint(currentPoint, chooseFernPoint(shapeList))
        cv2.imshow('frame', myShape)
        if cv2.waitKey(1) == ord("q"):
            break
    return 0


def main():
    print "Please enter divisor :"
    div = float(raw_input())
    for i in range(3, 8):
        generateChaoticShape(i, div)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
