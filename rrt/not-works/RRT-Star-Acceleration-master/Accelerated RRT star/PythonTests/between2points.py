import math
import numpy as np
import cv2
#input: image_extended, half width of driver, point1 ,point2
#output: if there is obstacle between 2 points- return any point on the obstacle.
#           the coordiantes of the returned point is according to image_extended
#        if not- return False
RADIAN=57.2957795
def findObstBetween2Points(img,halfWidth,point1,point2):

    theta = math.atan2(point1.y - point2.y, point1.x -point2.x)# direction to random XY
    theta*=RADIAN
    arrayPointsRectangle = []
    # Append empty lists in first two indexes.
    arrayPointsRectangle.append([])
    arrayPointsRectangle.append([])
    arrayPointsRectangle.append([])
    arrayPointsRectangle.append([])
    theta1Side=(theta+90)/RADIAN    # angle 90 degree to other point
    # Add elements to empty lists.
    arrayPointsRectangle[0].append(np.int0(point1.x+ halfWidth* math.cos(theta1Side))) #x point 1
    arrayPointsRectangle[0].append(np.int0(point1.y+ halfWidth* math.sin(theta1Side))) #y point 1

    arrayPointsRectangle[1].append(np.int0(point2.x+ halfWidth* math.cos(theta1Side))) #x point 2
    arrayPointsRectangle[1].append(np.int0(point2.y+ halfWidth* math.sin(theta1Side))) #y point 2

    theta2Side=(theta-90)/RADIAN # side 2 of theta.

    arrayPointsRectangle[2].append(np.int0(point1.x+ halfWidth* math.cos(theta2Side))) #x point 3
    arrayPointsRectangle[2].append(np.int0(point1.y+ halfWidth* math.sin(theta2Side))) #y point 3

    arrayPointsRectangle[3].append(np.int0(point2.x+ halfWidth* math.cos(theta2Side))) #x point 4
    arrayPointsRectangle[3].append(np.int0(point2.y+ halfWidth* math.sin(theta2Side))) #y point 4

    #now, get top left  ROI point:
    minxROI=min(arrayPointsRectangle[0][0],arrayPointsRectangle[1][0],arrayPointsRectangle[2][0],arrayPointsRectangle[3][0])-1   # top left ROI
    minyROI=min(arrayPointsRectangle[0][1],arrayPointsRectangle[1][1],arrayPointsRectangle[2][1],arrayPointsRectangle[3][1])-1

    # now, get bottom right ROI point: 
    maxxROI=max(arrayPointsRectangle[0][0],arrayPointsRectangle[1][0],arrayPointsRectangle[2][0],arrayPointsRectangle[3][0])+1   
    maxyROI=max(arrayPointsRectangle[0][1],arrayPointsRectangle[1][1],arrayPointsRectangle[2][1],arrayPointsRectangle[3][1])+1

    topLeftROI=(minxROI,minyROI)
    roi = img[minyROI:maxyROI,minxROI:maxxROI] # part of img
    mask = np.zeros((maxyROI-minyROI,maxxROI-minxROI), np.uint8)# all black
    x_p0RectInMask=arrayPointsRectangle[0][0]-minxROI# rotated (maybe) rect point  x in mask
    y_p0RectInMask=arrayPointsRectangle[0][1]-minyROI
    x_p1RectInMask=arrayPointsRectangle[1][0]-minxROI# rect point 
    y_p1RectInMask=arrayPointsRectangle[1][1]-minyROI
    x_p2RectInMask=arrayPointsRectangle[2][0]-minxROI# rect point 
    y_p2RectInMask=arrayPointsRectangle[2][1]-minyROI
    x_p3RectInMask=arrayPointsRectangle[3][0]-minxROI# rect point 
    y_p3RectInMask=arrayPointsRectangle[3][1]-minyROI
    cv2.line(mask,(x_p0RectInMask,y_p0RectInMask),(x_p1RectInMask,y_p1RectInMask),(255,255,255),1)
    cv2.line(mask,(x_p1RectInMask,y_p1RectInMask),(x_p2RectInMask,y_p2RectInMask),(255,255,255),1)
    cv2.line(mask,(x_p2RectInMask,y_p2RectInMask),(x_p3RectInMask,y_p3RectInMask),(255,255,255),1)
    cv2.line(mask,(x_p3RectInMask,y_p3RectInMask),(x_p0RectInMask,y_p0RectInMask),(255,255,255),1)#for the following line
    im2, cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #mask copy need?
    rect = cv2.minAreaRect(cnts[0])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(mask,[box],0,(255,255,255),-1)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
    indices = np.where(img1_bg == 255)
    if(indices[0].size == 0): 
        return False#safe
    return (topLeftROI[0]+indices[1][0],topLeftROI[1]+indices[0][0])#(y,x) in img_ext


