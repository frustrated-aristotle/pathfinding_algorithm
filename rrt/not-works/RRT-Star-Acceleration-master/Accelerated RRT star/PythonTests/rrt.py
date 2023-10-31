
import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import cv2
from itertools import product
import itertools
from random import choice
import itertools

show_animation = True
#our files:
from scopeROIobstacle import *
from minRectFromROI import *
from revealObstacle import *
from between2points import *
from extractRandom import *
ENOUGH_CLOSE_TO_GOAL = 150
class RRT():
    """
    Class for RRT Planning
    """

    def __init__(self, start, goal, obstacleList,widthOfDriver,centerDriver, randArea,im_th_extend,im_th_drawing_ext,
                 maxIter=150):
        """
        Setting Parameter
        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]
        """
        self.start = Node(start[0], start[1])# in im_th_extend image
        self.end = Node(goal[0], goal[1])#in im_th_extend image
        self.rows = randArea[0]  #in original image + bordersize
        self.columns = randArea[1]#in original image + bordersize
        self.maxIter = maxIter
        self.obstacleList = obstacleList
        self.widthOfDriver = widthOfDriver
        self.centerDriver = centerDriver     # x,y is in the extended image and radius of driver
        self.bordersize = randArea[2]# black border we added to margins of original image to prevent collusion when
             # the finding out of obstable size is near to  borders original image                               
        self.im_th_extend = im_th_extend
        self.im_th_drawing_ext = im_th_drawing_ext
        self.excluded = []
        self.counterObstacle = 1# just for console print.  can be deleted
        self.counterIteration=1 # just for console print.  can be deleted
        self.to_allow_range=list(itertools.product(range(self.bordersize, self.columns + 1), range(self.bordersize, self.rows + 1)))#the allowed range for random
 
       

    def Planning(self, animation=True):
        """
        Pathplanning
        animation: flag for animation on or off
        """
        animation=False;

        self.nodeList = [self.start]#array
        for i in range(self.maxIter):
            rnd = self.get_random_point()#random x y point
            nind = self.GetNearestListIndex(self.nodeList, rnd)#index of nearest x y in array
            newNode = self.steer(rnd, nind)#create newNode in the right direction to nearest
            nearNode = self.nodeList[nind]                           
            if animation:
                self.DrawGraph(rnd)
            if self.__CollisionCheck(newNode) and self.check_collision_extend(nearNode,newNode) :#false means there is collision
                nearinds = self.find_near_nodes(newNode)#no collision# return all points in tree that are neighbors of our new Node
                newNode = self.choose_parent(newNode, nearinds)
                self.nodeList.append(newNode)
                self.rewire(newNode, nearinds)

        # generate coruse
        lastIndex = self.get_best_last_index()
        if lastIndex is None:
            return None
        path = self.gen_final_course(lastIndex)
        return path

    def choose_parent(self, newNode, nearinds):
        if len(nearinds) == 0:
            return newNode
        dlist = []# prices for potential paths to NewNode
        for i in nearinds:# all neighbors of our new node
            dx = newNode.x - self.nodeList[i].x
            dy = newNode.y - self.nodeList[i].y
            d = math.sqrt(dx ** 2 + dy ** 2)
            if self.check_collision_extend(self.nodeList[i],newNode):#false means there is obstacle.  true is safe
                dlist.append(self.nodeList[i].cost + d)#no collision
            else:
                dlist.append(float("inf"))
        mincost = min(dlist)
        minind = nearinds[dlist.index(mincost)]
        if mincost == float("inf"):
            print("mincost is inf")
            return newNode
        newNode.cost = mincost
        newNode.parent = minind
        return newNode

    def steer(self, rnd, nind):

        # expand tree
        nearestNode = self.nodeList[nind]
        newNode = Node(rnd[0], rnd[1])
        dx = newNode.x - nearestNode.x
        dy = newNode.y - nearestNode.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        newNode.cost = nearestNode.cost + distance
        newNode.parent = nind # parent of NewNode = index in the array nodeList
        return newNode

    def get_random_point(self):
  
        random_point = random.choice( self.to_allow_range)
        print(self.counterIteration,"\\", self.maxIter," : " ,random_point)
        self.counterIteration+=1
        return random_point
      
       

    def get_best_last_index(self):# return index of the cheapest point that enough close to the destination

        disglist = [self.calc_dist_to_goal(node.x, node.y) for node in self.nodeList]# array of disance from all points to destination
        goalinds = [disglist.index(i) for i in disglist if i <= ENOUGH_CLOSE_TO_GOAL]# i= distance
        # goalinds contains the indexes of all good distances in disglis(
         # smaller than step size

        if len(goalinds) == 0:
            return None

        mincost = min([self.nodeList[i].cost for i in goalinds])# i=index in goalinds
        for i in goalinds:
            if self.nodeList[i].cost == mincost:
                return i
        return None

    def gen_final_course(self, goalind):
        path = [[self.end.x, self.end.y]]
        while self.nodeList[goalind].parent is not None:
            node = self.nodeList[goalind]
            path.append([node.x, node.y])
            goalind = node.parent
        path.append([self.start.x, self.start.y])
        return path

    def calc_dist_to_goal(self, x, y):
        return np.linalg.norm([x - self.end.x, y - self.end.y])

    def find_near_nodes(self, newNode):# return all points in tree that are neighbors of our new Node
        nnode = len(self.nodeList)
        r =20 +(180/nnode ** (1. / 3))
        dlist = [(node.x - newNode.x) ** 2 + (node.y - newNode.y) ** 2 for node in self.nodeList]
        nearinds = [dlist.index(i) for i in dlist if i <= r ** 2]
        return nearinds

    def rewire(self, newNode, nearinds):
        nnode = len(self.nodeList)
        for i in nearinds:
            nearNode = self.nodeList[i]
            dx = newNode.x - nearNode.x
            dy = newNode.y - nearNode.y
            d = math.sqrt(dx ** 2 + dy ** 2)
            scost = newNode.cost + d # maybe the new cost for the current near object
            if nearNode.cost > scost:
                if self.check_collision_extend(nearNode,newNode):#true is safe
                    nearNode.parent = nnode - 1# free way- nnode -1 is exactly newNode index
                    nearNode.cost = scost

    def check_collision_extend(self, nearNode, newNode):
        #return True if the way is free
        hasObstacle = findObstBetween2Points(self.im_th_extend,np.int0(self.widthOfDriver / 2),nearNode,newNode)#False is safe
        if(hasObstacle):#true here means there is obstacle
            if(not isAlreadyInRevealedObstacle(self,hasObstacle)):
               fromObstPoint_to_excludedRandom(self,hasObstacle)# huge function. recieved obstacle point and exclude obstacles points from random generator
            return False # collision

        return not hasObstacle # because we want that flase will be obstacle.  True is safe
        #if we got to this return- it's safe - return true
     

    def DrawGraph(self, rnd=None):
        plt.clf()
        thresh = self.im_th_drawing_ext.copy()# because we draw from begining in each iteration
        thresh = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)


           # get the axis
        for node in self.nodeList:
         if node.parent is not None:
            plt.plot([node.x, self.nodeList[node.parent].x], [node.y, self.nodeList[node.parent].y], "-g")#green
            dx = node.x - self.nodeList[node.parent].x
            dy = node.y - self.nodeList[node.parent].y
            d = math.sqrt(dx ** 2 + dy ** 2)
            if(d == 0):
                continue
            if(self.columns < 1500): #just for good presentation regarding to photo's size.
                cv2.arrowedLine(thresh, (self.nodeList[node.parent].x,self.nodeList[node.parent].y), (node.x,node.y), (255, 209, 0), 2,8,0,float(8) / d)
            else:
                cv2.arrowedLine(thresh, (self.nodeList[node.parent].x,self.nodeList[node.parent].y), (node.x,node.y), (255, 209, 0), 4,8,0,float(28) / d)
        
        for obstacle in self.obstacleList:
          if(self.columns < 1500):#just for good presentation regarding to photo's size.
             thresh = cv2.drawContours(thresh,[obstacle],0,(255,0,0),2)#
          else:
            thresh = cv2.drawContours(thresh,[obstacle],0,(255,0,0),3)#
         

        if rnd is not None:
            plt.plot(rnd[0], rnd[1], "xc")
        plt.plot(self.start.x, self.start.y, "bo")
        plt.plot(self.end.x, self.end.y, "ro")
        plt.axis([0,self.columns + self.bordersize, 0, self.rows + self.bordersize])
        plt.grid(True)
        ax = plt.gca()  
        ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis
        ax.xaxis.tick_top()                     # and move the X-Axis
        #ax.yaxis.set_ticks(np.arange(0, 16, 1)) # set y-ticks
                                   #ax.set_ylim(ay.get_ylim()[::-1])
        ax.yaxis.tick_left()     
        plt.imshow(thresh, cmap = 'gray', interpolation = 'bicubic')
        plt.show(block=False)
        plt.pause(0.0001)
        """
        Draw Graph
        """


    def GetNearestListIndex(self, nodeList, rnd):
        dlist = [(node.x - rnd[0]) ** 2 + (node.y - rnd[1]) ** 2 for node in nodeList]
        minind = dlist.index(min(dlist))
        return minind

    def __CollisionCheck(self, node):#newnode

        if(self.im_th_extend[node.y,node.x] == 255):#if it's obstacle
            im_floodfill = self.im_th_extend.copy()
            th, im_floodfill = cv2.threshold(im_floodfill, 127, 255, cv2.THRESH_BINARY_INV)#inv binary
            minRectPoints = fromObstPoint_to_minRect(im_floodfill,self.im_th_extend,node.x,node.y)
            goalInObstacle = IsPointInRevealedObstacle(minRectPoints,tuple([self.end.x,self.end.y]))#check if destination is in this obstacle
            if(goalInObstacle):# if it is - exit
                return
            self.obstacleList.append(minRectPoints)
            print("extract obstacle ",(self.counterObstacle) ," from random generator ")
            self.counterObstacle+=1#can delete- just for conosle print
            update_excluded(minRectPoints,self.excluded,self.to_allow_range)
            return False
        else:#now let's check if there is obstacle around this node
            hasObstaclePoint = findObstaclePointByRadius(self.im_th_extend,self.centerDriver[2],node)
              # findObstaclePointByRadius checks if there is no obstacle it return False.  if there is- it return x,y of
              # one white point in theo bstacle                                                                                                                                                                                                                                                                                                                  
            if(hasObstaclePoint != False):# there is obstacle.  so we have (x,y) in hasObstaclePoint
                 if(not isAlreadyInRevealedObstacle(self,hasObstaclePoint)):# because maybe we near the obstacle, not in it- so the driver can turn around there
                    fromObstPoint_to_excludedRandom(self,hasObstaclePoint)# huge function. recieved obstacle point and exclude obstacles points from random generator
                 return False   # collusion

        return True#safe- no collusion
class Node():
    """
    RRT Node
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0.0
        self.parent = None


def main():
    print("Start rrt planning")
    start = (70, 180)
    # ====Search Path with RRT====
    obstacleList = []  
    img = cv2.imread('path2.png')
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,im_th = cv2.threshold(imgray,127,255,0)# regular binary
    im_floodfill = im_th.copy()
    th, im_floodfill = cv2.threshold(im_floodfill, 127, 255, cv2.THRESH_BINARY_INV)#inv binary
    minRectPoints = fromObstPoint_to_minRect(im_floodfill,im_th,start[0],start[1])#return minRectangle of obstacle
    centerDriver = findCenterRadiusRectangle(minRectPoints)#return x,y,radius of center driver
    widthOfDriver = findFrontwidthDriver(minRectPoints)#return width of driver

    bordersize = centerDriver[2] + 1 #   add black border to margins of original image to prevent collusion when
                                     #  the finding of obstable size is near to  borders  original  image
    minRectPoints = np.int0(minRectPoints)#rectangle of driver
    im_th_algo = im_th.copy()
    cv2.drawContours(im_th_algo,[minRectPoints],0,(0,0,0),-1)#im_th_algo is without white in driver because it would fail the algo
    cv2.drawContours(im_th_algo,[minRectPoints],0,(0,0,0),2)#to delete border of driver
    im_th_drawing_ext = cv2.copyMakeBorder(im_th, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0])
    im_th_algo_ext = cv2.copyMakeBorder(im_th_algo, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0])
    centerDriver = [centerDriver[0] + bordersize,centerDriver[1] + bordersize,centerDriver[2]]
   # Set Initial parameters
    start = (bordersize + 70, bordersize + 180)
    rows,columns,channels = img.shape

    rrt = RRT(start, goal=[bordersize + 750, bordersize + 100],
       randArea=[bordersize + rows, bordersize + columns,bordersize], obstacleList=obstacleList,widthOfDriver=widthOfDriver,centerDriver=centerDriver,im_th_extend=im_th_algo_ext,im_th_drawing_ext=im_th_drawing_ext)
    path = rrt.Planning(animation=show_animation)
    try:
        # Draw final path
        print("The final path is (right to left) : ",[(x,y) for (x, y) in path])
        if show_animation:
            rrt.DrawGraph()
            plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')
            plt.grid(True)
            plt.pause(0.01)  # Need for Mac
            plt.show()

    except:
        print("*****\n\nThere is no path cause all points in the final tree are too far from the goal point \n\n*****")
       

if __name__ == '__main__':
    main()
