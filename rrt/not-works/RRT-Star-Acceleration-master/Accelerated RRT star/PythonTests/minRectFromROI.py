import numpy as np
import cv2
import math


#input: rectangle which return from cv2.minAreaRect
#output:the same object but the rectangle is slightly bigger
def getAwayFromEdge(rect):
    WidthHeightList=list(rect[1])# becuase tuple is unchangable so convert to list
    WidthHeightList[0]=WidthHeightList[0]+8 #extend the width. 8 is constant
    WidthHeightList[1]=WidthHeightList[1]+8 #extend the height. 8 is constant
    rectList=list(rect)
    rectList[1]=WidthHeightList;
    return tuple(rectList)

#thresh is the ROI ( part of whole image) and ofcourse Black&White
def findMinRect(thresh):
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE )
    maxIndex=findIndexBiggestContour(contours)# always return 0 ?
    rect = cv2.minAreaRect(contours[maxIndex])
    box = cv2.boxPoints(getAwayFromEdge(rect))
    box = np.int0(box)# convert to integer
    return box #return min rectangle of obstacle in ROI 

def findIndexBiggestContour(contours):#find biggest contour area size in contours list
    max=contours[0].size
    iMax=0
    iLoop=0
    for cont in contours:
        if cont.size>max:
            max=cont.size
            iMax=iLoop;
        iLoop=iLoop+1
    return iMax

def findCenterRadiusRectangle(box):#return ( (x1 +x2)/2 ,(y1 + y2)/2 ). of diagonal points and radius
    dx0=box[0][0]-box[1][0]
    dy0=box[0][1]-box[1][1]
    distance1=radiusOfDriver=math.sqrt(dx0 ** 2 + dy0 ** 2)
    dx1=box[0][0]-box[2][0]
    dy1=box[0][1]-box[2][1]
    distance2=radiusOfDriver=math.sqrt(dx1 ** 2 + dy1 ** 2)
    dx2=box[2][0]-box[1][0]
    dy2=box[2][1]-box[1][1]
    distance3=radiusOfDriver=math.sqrt(dx2 ** 2 + dy2 ** 2)
    maxDistance=max(distance1,distance2,distance3)
    radius=math.ceil(maxDistance/2)
    if(maxDistance==distance1):
        return (np.int0((box[0][0]+box[1][0])/2),np.int0((box[0][1]+box[1][1])/2),radius)
    if(maxDistance==distance2):
        return (np.int0((box[0][0]+box[2][0])/2),np.int0((box[0][1]+box[2][1])/2),radius)
    if(maxDistance==distance3):
        return (np.int0((box[2][0]+box[1][0])/2),np.int0((box[1][1]+box[1][1])/2),radius)
        

def findFrontwidthDriver(box):#find min width of driver rectangle (that we made)
    dx0=box[0][0]-box[1][0]
    dy0=box[0][1]-box[1][1]
    distance1=math.sqrt(dx0 ** 2 + dy0 ** 2)
    dx1=box[0][0]-box[2][0]
    dy1=box[0][1]-box[2][1]
    distance2=math.sqrt(dx1 ** 2 + dy1 ** 2)
    dx2=box[2][0]-box[1][0]
    dy2=box[2][1]-box[1][1]
    distance3=math.sqrt(dx2 ** 2 + dy2 ** 2)
    return np.int0(min(distance1,distance2,distance3))
