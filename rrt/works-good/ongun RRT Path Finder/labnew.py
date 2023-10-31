import pygame
import sys, random, math, time
from pygame.locals import *
from math import sqrt,cos,sin,atan2

# This program generates a simple rapidly
# exploring random tree (RRT) in a rectangular region, with obstacles

class Node(object):
    """Node in a tree"""
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

def dist(p1,p2): #dis function calculates the distanceanceanceanceance btw two points
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision(p1, p2, radius): #if radius is bigger than distance btw two points return true 
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

#constants
XDIM = 720
YDIM = 500
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 50000
GOAL_RADIUS = 10 #the end point (goal)' radius used to calculate whether we reached the goal or not. 
MIN_DISTANCE_TO_ADD = 1.0
GAME_LEVEL = 1
white = (255, 240, 200)
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,255,255
berkay1=36,123,160
berkay2=112,193,179
berkay3=178,219,191
berkay4=243,255,189
berkay5=255,22,84

pygame.init()
fpsClock = pygame.time.Clock()

#initialize and prepare screen
screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption('Rapidly Exploring Random Tree - RRT algorithm - Berkay ERSOY & Ongun DEMIRAG')

# setup program variables
count = 0
rectObs = []
circObs = []
def step_from_to(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def collides(p):
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            # print ("collision with object: " + str(rect))
            return True
    for circle in circObs:
        if circle.collidepoint(p) == True:
            # print ("collision with object: " + str(rect))
            return True
    return False

def get_random():
    return random.random()*XDIM, random.random()*YDIM

def get_random_clear():
    while True:
        p = get_random()
        noCollision = collides(p)
        if noCollision == False:
            return p

def init_obstacles(configNum): #creates obstacles dependant on configuration
    global rectObs
    global circObs
    rectObs = []
    circObs = []

    font = pygame.font.SysFont("Trecbuchet MS" , 25)
    Bottom_text = font.render("Config:" + str(configNum) + ". Berkay Ersoy - Ongun Demirağ - 2019 ", 1 , white)
    Bottem_text_Rect = Bottom_text.get_rect()
    Bottem_text_Rect.center = (515,490)
    screen.blit(Bottom_text,Bottem_text_Rect)
    pygame.display.flip()

    if (configNum == 0):
        rectObs.append(pygame.Rect((XDIM / 2.0 - 50, YDIM / 2.0 - 100),(100,200)))
    if (configNum == 1): 
        rectObs.append(pygame.Rect((200,250),(10,200)))    # Rect(left, top, width, height) -> Rect             
        rectObs.append(pygame.Rect((500,200),(50,200)))
        rectObs.append(pygame.Rect((200,250),(200,10)))

        rectObs.append(pygame.Rect((0,0),(720,10))) #top frame
        rectObs.append(pygame.Rect((0,0),(10,720))) #left frame
        rectObs.append(pygame.Rect((0,470),(720,10))) #bottom frame
        rectObs.append(pygame.Rect((710,0),(10,720))) #right frame
       
       # circObs.append(pygame.circle((250,250), 5))
        circObs.append(pygame.draw.circle(screen, berkay1, (250,100), 50))
    if (configNum == 2):
        rectObs.append(pygame.Rect((40,10),(100,200)))
    if (configNum == 3):
        rectObs.append(pygame.Rect((40,10),(100,200)))
    for rect in rectObs: #for more than one rectangular obstacles
        pygame.draw.rect(screen, berkay1, rect)
        #pygame.draw.circle(screen, berkay1, circle)

def reset(): #initialize variables like background color and game difficulty
    global count
    screen.fill(black) # BACKGROUND COLOR
    init_obstacles(GAME_LEVEL)
    count = 0


def main():
    global count

    initPoseSet = False
    initialPoint = Node(None, None)
    goalPoseSet = False
    goalPoint = Node(None, None)
    currentState = 'init'

    nodes = []
    reset()

    while True:
        if currentState == 'init':
            print('Please set a goal point!')
            fpsClock.tick(10)
            
        elif currentState == 'goalFound':
            #traceback
            currNode = goalNode.parent
            while currNode.parent != None: # Goal Found time to draw the path.
                pygame.draw.line(screen,berkay5,currNode.point,currNode.parent.point,3) #calculated path. 
                currNode = currNode.parent
            optimizePhase = True
        elif currentState == 'optimize':
            fpsClock.tick(0.5)
            pass
        elif currentState == 'buildTree':
            count = count+1
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    # print("random num = " + str(rand))
                    parentNode = nodes[0]

                    for p in nodes: #find nearest vertex
                        if dist(p.point,rand) <= dist(parentNode.point,rand): #check to see if this vertex is closer than the previously selected closest
                            newPoint = step_from_to(p.point,rand)
                            if collides(newPoint) == False: # check if a collision would occur with the newly selected vertex
                                parentNode = p #the new point is not in collision, so update this new vertex as the best
                                foundNext = True

                newnode = step_from_to(parentNode.point,rand)
                nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen,berkay4,parentNode.point,newnode)


                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                    currentState = 'goalFound'
                    end = time.time()
                    print("Total Time elapsed:" , str(round(end-start,2)))
                    goalNode = nodes[len(nodes)-1]
                    Font = pygame.font.SysFont("Trebuchet MS", 15)
                    DayFont = Font.render("Node: " +str(count)+ ".Total Time elapsed: " +str(round(end-start,2))+ "s.", 1 , white)
                    DayFontR=DayFont.get_rect()
                    DayFontR.center=(135,490)
                    screen.blit(DayFont, DayFontR)
                    pygame.display.flip()
 


            else:
                print("Ran out of nodes... :(")
                return;

        #handle events
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")

            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if currentState == 'init':
                    if initPoseSet == False:
                        nodes = []
                        if collides(e.pos) == False:
                            #print('initiale pose set: '+str(e.pos))

                            initialPoint = Node(e.pos, None)
                            nodes.append(initialPoint) # Start in the center
                            initPoseSet = True
                            pygame.draw.circle(screen, white, initialPoint.point, GOAL_RADIUS)   # STARTING NODEEE
                    elif goalPoseSet == False:
                        #print('goal pose set: '+str(e.pos))
                        start = time.time()
                   
                        if collides(e.pos) == False:
                            goalPoint = Node(e.pos,None)
                            goalPoseSet = True
                            pygame.draw.circle(screen, berkay5, goalPoint.point, GOAL_RADIUS)   # END NODEEEE 
                            currentState = 'buildTree'
                else:
                    currentState = 'init'
                    initPoseSet = False
                    goalPoseSet = False
                    reset()

        pygame.display.update()
        fpsClock.tick(10000)


# if python says run, then we should run
if __name__ == '__main__':
    main()
    input("press Enter to quit")

    