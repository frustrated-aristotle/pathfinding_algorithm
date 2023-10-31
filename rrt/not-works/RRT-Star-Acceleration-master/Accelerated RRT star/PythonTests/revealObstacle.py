from scopeROIobstacle import *
from minRectFromROI import *
from extractRandom import *

#very huge function. this func uses other functions we built.
#input: obstacle point
#output: void. excluded points in obstacle from random generator
def fromObstPoint_to_excludedRandom(self,hasObstaclePoint):
    im_floodfill = self.im_th_extend.copy()
    th, im_floodfill = cv2.threshold(im_floodfill, 127, 255, cv2.THRESH_BINARY_INV)#inv binary
    minRectPoints = fromObstPoint_to_minRect(im_floodfill,self.im_th_extend,hasObstaclePoint[0],hasObstaclePoint[1])#includes many other functions we built
    goalInObstacle = IsPointInRevealedObstacle(minRectPoints, tuple([self.end.x,self.end.y]))#check if destination is in this obstacle
    if(goalInObstacle):# if it is - exit
        return
    self.obstacleList.append(minRectPoints)
    print("extract obstacle ",(self.counterObstacle) ," from random generator ")
    self.counterObstacle+=1#can delete- just for conosle print
    update_excluded(minRectPoints,self.excluded,self.to_allow_range)



#very big function. this func uses other functions we built.
#input: im_floodfill ,im_th_extend,node (we know the node is white ( in obstacle))
#output: min rectangle of this obstacle
#in parameters: im_th_extend can be not the extended version
def fromObstPoint_to_minRect(im_floodfill,im_th_extend,nodeX,nodeY):
    rectangleROIdriver=findROI(im_floodfill,(nodeX,nodeY))#return  x,y of ROI and w,h. not the image 
    ROIRectx=rectangleROIdriver[0] #top left x of ROI
    ROIRecty=rectangleROIdriver[1] #top left y of ROI
    imgBinaryROI=im_th_extend[ROIRecty-1:ROIRecty+rectangleROIdriver[3]+1,ROIRectx-1:ROIRectx+rectangleROIdriver[2]+1]#img binary of ROI
    minRectPoints=findMinRect(imgBinaryROI)#return end points of minRect
    for i in range(0, 4):
        minRectPoints[i][0]=minRectPoints[i][0]+ROIRectx
        minRectPoints[i][1]=minRectPoints[i][1]+ROIRecty
    return minRectPoints


#input: binaryImage,radius of driver, node in the img_th
#output: point x,y of obstacle ( if so ) in the image_ext
def findObstaclePointByRadius(img_ext_th,radiusDriver,node): #return x,y of white point in roi
    topLeftROI=(node.x-radiusDriver,node.y-radiusDriver)
    roi = img_ext_th[node.y-radiusDriver:node.y+radiusDriver,node.x-radiusDriver:node.x+radiusDriver] #// part of img
    mask = np.zeros((2*radiusDriver,2*radiusDriver), np.uint8)# // all black
    cv2.circle(mask,(radiusDriver,radiusDriver), radiusDriver, (255,255,255), -1)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
    indices = np.where(img1_bg == [255])
    if(indices[0].size == 0):
        return False
    return (topLeftROI[0]+indices[1][0],topLeftROI[1]+indices[0][0]) # indices[0] is an array of all y coordinate ; indices[1] is an array of all x coordinate
# return point x,y of obstacle ( if so ) in the image_ext


#input: 4 points of obstacle, and point
#output: true if point is in obstacle. else : Flase
def IsPointInRevealedObstacle(points4obstacle,point):
    ctr=np.array([points4obstacle[0],points4obstacle[1],points4obstacle[2],points4obstacle[3]])# build contour form 4 points
    indicator = cv2.pointPolygonTest(ctr, point, False); #-1 is outside
    indicator = np.int0(indicator)
    if indicator==-1:
        return False#point is not in obstacle
    return True

#input: point
#output: true is we already revealed this obstacle. else return false
def isAlreadyInRevealedObstacle(self,hasObstaclePoint):
    for  points4obstacle in self.obstacleList:
        isAlreadyInRevealedObstacle = IsPointInRevealedObstacle(points4obstacle,hasObstaclePoint)#False means point is not in obstacle
        if(isAlreadyInRevealedObstacle == True):# because maybe we got random point that is very close to
             return True;       # our obstacle( not on it!) so the driver can't drive there and turn
                                # around
    return False; # we didn't yet reveal this obstacle