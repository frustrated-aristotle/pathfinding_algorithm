import pygame
import time
import os
import sys
sys.path.append('..')

from RRT_Star import RRTGraph
from RRT_Star import RRTMap
from Robot_bicycle_model import Robot


# Select True for RRT Star or False for regular RRT
RRT_STAR = True
# UPDATE your project folder before running
Projectfolder_image = '/path/to/image'


Background = os.path.join(Projectfolder_image, 'background.jpg')
Body_Robot = os.path.join(Projectfolder_image, 'Body.png')
Wheel_Robot = os.path.join(Projectfolder_image,'wheel.png')
car = pygame.image.load(os.path.join(Projectfolder_image, 'car.png'))
car2 = pygame.image.load(os.path.join(Projectfolder_image, 'car2.png'))
car3 = pygame.image.load(os.path.join(Projectfolder_image, 'car3.png'))
police = pygame.image.load(os.path.join(Projectfolder_image, 'police.png'))

dimensions = (1000, 1000) # -y x
start = (25, 50)
goal = (790, 950) # x -y
obsdim = 35
obsnum = 17
number_iterations= 1000
iteration=0

def main1():

    iteration=0
    pygame.init()
    map = RRTMap(start,goal,dimensions,obsdim,obsnum)
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum, RRT_STAR)
    obstacles, obstaclesbbox = graph.makeobs()
    map.drawMapObs(obstacles, obstaclesbbox)

    X = []
    t1 = time.time()

    while (iteration < number_iterations):
        if X != []:
            map.undrawEdges(X, Y, Parents)

        # time.sleep(0.5)
        elapsed = time.time() - t1
        t1 = time.time()

        if elapsed > 20:
            raise

        if iteration % 100 == 0:
            X, Y, Parents = graph.bias(goal)
            map.drawStuff(X, Y, Parents)


        else:
            X, Y, Parent = graph.expand()
            map.drawStuff(X, Y, Parents)

        if iteration % 5 == 0:
            pygame.display.update()
        iteration += 1

        if graph.reroutepathFlag:
            reroutedpath = graph.getPathCoords()
            map.drawPath(firstpath, (255, 255, 255), 8)
            map.drawPath(reroutedpath, (0, 255, 0), 8)
            firstpath = reroutedpath
            graph.reroutepathFlag = False

        graph.path_to_goal()
        if graph.goalFlag:
            firstpath = graph.getPathCoords()
            map.drawPath(firstpath, (255, 0, 0), 8)
            graph.goalFlag = False
            print('The first path is found in iteration:', iteration)
            print('average time per iteration (ms)', pygame.time.get_ticks() / (iteration))
            graph.get_path_length()
            print('Number of nodes placed till first path', len(X))


        graph.change_path_to_goal()
        if graph.changeFlag:
            newpath = graph.getPathCoords()
            map.drawPath(firstpath, (255, 255, 255), 8)
            map.drawPath(newpath, (0, 255, 0), 8)
            firstpath = newpath
            graph.changeFlag = False
            graph.goalFlag = False


        pygame.event.wait(5)



        pygame.display.update()

        pygame.event.clear()
        if iteration == number_iterations:
            path = graph.getPathCoords()
            print('finised at iteration:', iteration)
            print('average time per iteration (ms)', pygame.time.get_ticks() / (iteration))
            graph.get_path_length()
            print('Number of nodes placed at final path', len(X))

    return path

def main2(path):

    lasttime = pygame.time.get_ticks()
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum,RRT_STAR)

    obstacles, obstaclesbbox = graph.makeobs()
    map.drawMapObs(obstacles, obstaclesbbox)
    def Drawcars(car,car2,car3,police):

        car = pygame.transform.scale(car, (150, 80))
        car2 = pygame.transform.scale(car2, (150, 80))

        car3 = pygame.transform.rotate(car3, -90)
        car3 = pygame.transform.scale(car3, (150, 80))

        police = pygame.transform.rotate(police, 90)
        police = pygame.transform.scale(police, (150, 80))

        map.map.blit(car3, (440, 610))
        map.map.blit(car2, (440, 710))
        map.map.blit(car, (440, 810))
        map.map.blit(car2, (440, 910))

        car = pygame.transform.rotate(car, 180)
        car2 = pygame.transform.rotate(car2, 180)

        car3 = pygame.transform.rotate(car3, 180)

        map.map.blit(car, (295, 10))
        map.map.blit(car2, (295, 110))
        map.map.blit(car3, (295, 210))
        map.map.blit(car2, (295, 310))

        map.map.blit(car, (645, 10))
        map.map.blit(car2, (645, 110))
        map.map.blit(car, (645, 610))
        map.map.blit(car2, (645, 710))
        map.map.blit(police, (645, 810))


    def robot_simulate(dt, event=None):
        robot.move(dt, event=event)
        robot.draw(map.map)

    path = path
    path.reverse()
    x_path=[]
    y_path=[]
    for x in path:
        x_path.append(x[0])
        y_path.append(x[1])

    map.removebbox(obstacles, obstaclesbbox)

    map.drawPath(path,(255, 0, 0), 5)

    Drawcars(car,car2,car3,police) # Draw the cars on the background

    pygame.image.save(map.map,Background)
    robot = Robot(start, x_path, y_path, Body_Robot, Wheel_Robot, 80,Background)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if running == False:
                pygame.quit()
        pygame.display.update()
        dt = (pygame.time.get_ticks() - lasttime) / 1000
        lasttime = pygame.time.get_ticks()
        robot_simulate(dt)
        running = robot.carfoundgoal()

if __name__ == '__main__':
    path = main1()
    main2(path)
