import time
import pygame
from grid import OccupancyGridMap
from typing import List
from turning_point_finder import TurningPointFinder

# Define some colors
BLACK = (0, 0, 0)  # BLACK
UNOCCUPIED = (255, 255, 255)  # WHITE
GOAL = (0, 255, 0)  # GREEN
START = (255, 0, 0)  # RED
GRAY1 = (145, 145, 102)  # GRAY1
OBSTACLE = (77, 77, 51)  # GRAY2
LOCAL_GRID = (0, 0, 80)  # BLUE
TURNING_POINT = (33, 100, 119)  # PETROLEUM BLUE
CURRENT = (223, 28, 237)  # PURPLE

colors = {
    0: UNOCCUPIED,
    1: GOAL,
    255: OBSTACLE
}

def engeller(self, row,col):
    # change the x/y screen coordinates to grid coordinates
    x = row // (self.height + self.margin)
    y = col // (self.width + self.margin)

    # turn pos into cell
    grid_cell = (x, y)

    # set the location in the grid map
    if self.world.is_unoccupied(grid_cell):
        self.world.set_obstacle(grid_cell)
        self.observation = {"pos": grid_cell, "type": OBSTACLE}


class Animation:

    path = []
    turning_point_finder = TurningPointFinder(path=path)

    counter = 0
    #Is there any difference between 60 hz and 144 hz
    def __init__(self,
                 title="D* Lite Path Planning",
                 width=10,
                 height=10,
                 margin=0,
                 x_dim=100,
                 y_dim=50,
                 start=(0, 0),
                 goal=(50, 50),
                 viewing_range=10):

        self.width = width
        self.height = height
        self.margin = margin
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.start = start
        self.current = start
        self.observation = {"pos": None, "type": None}
        self.goal = goal
        self.viewing_range = viewing_range
        self.turning_points = []
        
        pygame.init()

        # Set the 'width' and 'height' of the screen
        window_size = [(width + margin) * y_dim + margin,
                       (height + margin) * x_dim + margin]

        self.screen = pygame.display.set_mode(window_size)

        # create occupancy grid map
        """
        set initial values for the map occupancy grid
        |----------> y, column
        |           (x=0,y=2)
        |
        V (x=2, y=0)
        x, row
        """
        self.world = OccupancyGridMap(x_dim=x_dim,
                                      y_dim=y_dim,
                                      exploration_setting='8N')

        # Set title of screen
        pygame.display.set_caption(title)

        # set font
        pygame.font.SysFont('Comic Sans MS', 36)
        self.default_engeller()


        # Loop until the user clicks the close button
        self.done = False

        # used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def get_position(self):
        return self.current

    def set_position(self, pos: (int, int)):
        self.current = pos

    def get_goal(self):
        return self.goal

    def set_goal(self, goal: (int, int)):
        self.goal = goal

    def set_start(self, start: (int, int)):
        self.start = start

    @staticmethod
    def center_pos(width, margin, height, coordinate_tuple) -> (int, int):
        x = coordinate_tuple[0]
        y = coordinate_tuple[1]
        step_center = [round(y * (width + margin) + width / 2) + margin,
                               round(x * (height + margin) + height / 2) + margin]
        return step_center


    def display_path(self, path=None):
        if path is not None:
            for step in path:
                # draw a moving robot, based on current coordinates
                step_center = Animation.center_pos(self.width, self.margin, self.height, step)
                #step_center = [round(step[1] * (self.width + self.margin) + self.width / 2) + self.margin,
                #               round(step[0] * (self.height + self.margin) + self.height / 2) + self.margin]

                if step is self.current:
                    pygame.draw.circle(self.screen, CURRENT, step_center, round(self.width / 2) - 2)
                else:
                    pygame.draw.circle(self.screen, START, step_center, round(self.width / 2) - 2)


    def display_obs(self, observations=None):
        if observations is not None:
            for o in observations:
                pygame.draw.rect(self.screen, GRAY1, [(self.margin + self.width) * o[1] + self.margin,
                                                      (self.margin + self.height) * o[0] + self.margin,
                                                      self.width,
                                                      self.height])

    def on_space_clicked(self, path):
        print("Space Button is clicked!")
        (x, y) = path[1]
        self.set_position((x, y))
       

    def get_turning_points(self, path):
        self.turning_point_finder.find_turning_points(path)
        self.turning_points = self.turning_point_finder.turning_points

    def draw_rounding_points(self, path):
        self.get_turning_points(path=path)
        if len(self.turning_points) > 0:
            for point in self.turning_points:
                point_center = Animation.center_pos(self.width, self.margin, self.height, point)
                pygame.draw.circle(self.screen, TURNING_POINT, point_center, round(self.width / 2) - 2)
                


    def run_game(self, path=None):
        if path is None:
            path = []

        grid_cell = None
        self.cont = False

        # get inputs from keyboard and
        self.input_validation(path)
        # set the screen background
        self.screen.fill(BLACK)

        # draw the grid
        self.draw_grid()
        self.display_path(path=path)
        self.draw_rounding_points(path=path)
        self.draw_goal()
        self.draw_current_cell()
        self.draw_range()   
        # set game tick
        self.clock.tick(20)

        # go ahead and update screen with that we've drawn
        pygame.display.flip()
    # be 'idle' friendly. If you forget this, the program will hang on exit
    pygame.quit()
    
    def input_validation(self, path):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # if user clicked close
                print("quit")
                self.done = True  # flag that we are done so we can exit loop

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or self.cont:
                # space bar pressed. call next action
                if path:
                    self.on_space_clicked(path)
            
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_i):
                print("Carry your robot to where you want!")
                tuple_str = input("Type its point like (x,y) int tuple)")
                tuple_list = tuple_str.split(",")
                tuple_input = (int(tuple_list[0]), int(tuple_list[1]))
                print(type(tuple_input), tuple_input)
                self.set_position(tuple_input)

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_m):
                tuple_str = input("Obstacle point like (x,y) int tuple)")
                tuple_list = tuple_str.split(",")
                tuple_input = (int(tuple_list[0]), int(tuple_list[1]))
                print(type(tuple_input), tuple_input)
                self.add_obstacle(tuple_input)


            # set obstacle by holding left-click
            elif pygame.mouse.get_pressed()[0]:
                self.add_obstacle()

            # remove obstacle by holding right-click
            elif pygame.mouse.get_pressed()[2]:
                self.remove_obstacle()
            
    def draw_grid(self):

        for row in range(self.x_dim):
            for column in range(self.y_dim):
                # color the cells
                pygame.draw.rect(self.screen, colors[self.world.occupancy_grid_map[row][column]],
                                 [(self.margin + self.width) * column + self.margin,
                                  (self.margin + self.height) * row + self.margin,
                                  self.width,
                                  self.height])
    
    def draw_goal(self):
        # fill in the goal cell with green
        pygame.draw.rect(self.screen, GOAL, [(self.margin + self.width) * self.goal[1] + self.margin,
                                             (self.margin + self.height) * self.goal[0] + self.margin,
                                             self.width,
                                             self.height])

    def draw_current_cell(self):
        # pygame.draw.circle(self.screen, START, robot_center, round(self.width / 2) - 2)
        robot_center = Animation.center_pos(self.width, self.margin,self.height,self.current)
        pygame.draw.circle(self.screen, CURRENT, robot_center, round(self.width / 2) - 2)

    def draw_range(self):
        # draw robot local grid map (viewing range)
        robot_center = Animation.center_pos(self.width, self.margin,self.height,self.current)
        pygame.draw.rect(self.screen, LOCAL_GRID,
                         [robot_center[0] - self.viewing_range * (self.height + self.margin),
                          robot_center[1] - self.viewing_range * (self.width + self.margin),
                          2 * self.viewing_range * (self.height + self.margin),
                          2 * self.viewing_range * (self.width + self.margin)], 2)

    def add_obstacle(self):
        # User clicks the mouse. Get the position
        (col, row) = pygame.mouse.get_pos()

        # change the x/y screen coordinates to grid coordinates
        x = row // (self.height + self.margin)
        y = col // (self.width + self.margin)

        # turn pos into cell
        grid_cell = (x, y)

        # set the location in the grid map
        if self.world.is_unoccupied(grid_cell):
            self.world.set_obstacle(grid_cell)
            self.observation = {"pos": grid_cell, "type": OBSTACLE}
        print(row, col)

    def remove_obstacle(self):
        # User clicks the mouse. Get the position
        (col, row) = pygame.mouse.get_pos()

        # change the x/y screen coordinates to grid coordinates
        x = row // (self.height + self.margin)
        y = col // (self.width + self.margin)

        # turn pos into cell
        grid_cell = (x, y)

        # set the location in the grid map
        if not self.world.is_unoccupied(grid_cell):
            print("grid cell: ".format(grid_cell))
            self.world.remove_obstacle(grid_cell)
            self.observation = {"pos": grid_cell, "type": UNOCCUPIED}
        
    def default_engeller(self):
            
            engeller(self,103,128)
            engeller(self,144,132)
            engeller(self,140,106)
            engeller(self,103,96)

            engeller(self,261,96)
            engeller(self,266,140)
            engeller(self,293,95)
            engeller(self,296,138)

            engeller(self,401,96)
            engeller(self,413,140)
            engeller(self,476,142)
            engeller(self,458,93)

            # orta_ust
            # engeller(self,144,304)
            engeller(self,94,265)
            engeller(self,139,262)
            engeller(self,113,309)

            # merkez
            # engeller(self,258,296)
            engeller(self,260,261)
            engeller(self,287,257)
            engeller(self,288,297)

            engeller(self,414,256)
            engeller(self,452,255)
            engeller(self,457,299)
            engeller(self,417,296)

            # sag_üst
            # engeller(self,123,416)
            engeller(self,92,418)
            engeller(self,130,457)
            engeller(self,106,457)

            # sag_orta
            # engeller(self,255,420)
            engeller(self,282,421)
            engeller(self,296,441)
            engeller(self,270,453)

            engeller(self,419,412)
            engeller(self,444,411)
            engeller(self,423,448)
            engeller(self,461,446)

            # kavsak
            engeller(self,189,345)
            engeller(self,217,344)
            engeller(self,184,379)
            engeller(self,217,370)