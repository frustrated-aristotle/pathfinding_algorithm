from re import S
import copy
import pygame
from path_finding import a_star
from path_finding import d_star_lite, move_and_rescan


TOP_MENU_HEIGHT = 0.025 #perc
WIN_WIDTH = 800
WIN_HEIGHT = WIN_WIDTH + int((WIN_WIDTH * (TOP_MENU_HEIGHT)))
# MAIN_GRID_HEIGHT = MAIN_GRID_WIDTH - (MAIN_GRID_WIDTH * (TOP_MENU_HEIGHT))
SCAN_RANGE = 1

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")
pygame.font.init()

RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BROWN = (150, 75, 0)


class Grid:
	def __init__(self, rows, width, start_coord, end_coord):
		self.gap = width // rows
		self.width = width
		self.rows = rows
		self.start_x, self.start_y = start_coord
		self.end_x, self.end_y = end_coord
		self.grid = []

	def make_grid(self):
		for i in range(self.rows):
			self.grid.append([])
			for j in range(self.rows):
				spot = Spot(i, j,self.gap, self.rows, (self.start_x, self.start_y, self.end_x, self.end_y))
				self.grid[i].append(spot)
	
	def reset_grid(self):
		self.grid = []
		self.make_grid()

	def reset_search_area(self):
		for row in self.grid:
			for spot in row:
				if spot.is_open() or spot.is_closed() or spot.is_path():
					spot.reset()

	def get_grid(self):
		return self.grid

	def get_spot(self, row=None, col=None, x=None, y=None):
		if row and col:
			return self.grid[row][col]
		elif x and y:
			x = x - self.start_x
			y = y - self.start_y
			row = y // self.gap
			col = x // self.gap
			print(f"spot : [{row}][{col}]")
			return self.grid[row][col]
		else:
			pass
			#TODO: add exception

	def draw_grid(self, win):
		for i in range(self.rows):
			pygame.draw.line(win, GREY, (self.start_x, self.start_y + (i * self.gap)), (self.end_x, self.start_y + (i * self.gap)))
		for j in range(self.rows):	
			pygame.draw.line(win, GREY, (self.start_x + (j * self.gap), self.start_y), (self.start_x + (j * self.gap), self.end_y))				

class Rectangle:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = BLACK
	
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))	

	def draw_text(self, win, text, size, color, pos):
		# print(text, size, color, pos)
		font = pygame.font.SysFont("Comic Sans MS", size, True)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect(topleft=pos)
		win.blit(text_surface, text_rect)

class TopBar(Rectangle):
	def __init__(self, x, y, width, height):
		self.current_mode = "DESIGN"
		self.alg = ""
		self.mode_string_pos = (x+5,y+2)
		# self.alg_string_pos = (x+200,y+2)
		self.mode_string_size = 10
		self.mode_string_color = WHITE
		super().__init__(x, y, width, height)
	
	def update_mode(self, win, mode):
		self.current_mode = mode 
		self.draw(win)
		self.draw_text(win, f"MODE: {self.current_mode}", self.mode_string_size, self.mode_string_color, self.mode_string_pos)

	def update_alg(self, win, alg):
		pass
		# self.alg = alg
		# self.draw(win)
		# self.draw_text(win, f"ALGORITHM: {self.alg}", self.mode_string_size, self.mode_string_color, self.alg_string_pos)

class Spot:
	def __init__(self, row, col, width, total_rows, grid_coord, g=None, rhs=None):
		self.row = row
		self.col = col
		self.g = g
		self.rhs = rhs
		### cant be absolute X,Y
		self.x_start, self.y_start, self.x_end, self.y_end = grid_coord
		self.x = self.x_start + (col * width)
		self.y = self.y_start + (row * width)
		# self.x =  (row * width)
		# self.y =  (col * width)
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK
	
	def is_object(self):
		return self.color == GREY

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def is_path(self):
		return self.color == PURPLE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_object(self):
		self.color = GREY

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
		# font = pygame.font.SysFont("Comic Sans MS", 15, True)
		# text_color = BLACK if self.color == WHITE else WHITE
		# text_surface = font.render(f"({self.row}, {self.col})", True, text_color)
		# text_rect = text_surface.get_rect(topleft=(self.x+5, self.y+5))
		# win.blit(text_surface, text_rect)
		# text_surface = font.render(f"x: {self.x}, y: {self.y}", True, text_color)
		# text_rect = text_surface.get_rect(topleft=(self.x+5, self.y+20))
		# win.blit(text_surface, text_rect)
		# text_surface = font.render(f"g: {self.g}", True, text_color)
		# text_rect = text_surface.get_rect(topleft=(self.x+5, self.y+40))
		# win.blit(text_surface, text_rect)
		# text_surface = font.render(f"rhs: {self.rhs}", True, text_color)
		# text_rect = text_surface.get_rect(topleft=(self.x+5, self.y+55))
		# win.blit(text_surface, text_rect)

		# text_surface = font.render(f"col: {self.col}", True, text_color)
		# text_rect = text_surface.get_rect(topleft=(self.x+5, self.y+65))
		# win.blit(text_surface, text_rect)

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier() and not grid[self.row + 1][self.col].is_object(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier() and not grid[self.row - 1][self.col].is_object(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier() and not grid[self.row][self.col + 1].is_object(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier() and not grid[self.row][self.col - 1].is_object(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

		# if self.row < self.total_rows - 1:
		# 	if grid[self.row + 1][self.col].is_barrier() or grid[self.row + 1][self.col].is_object(): # DOWN
		# 		self.neighbors[grid[self.row + 1][self.col]] = float("inf")
		# 	else:
		# 		self.neighbors[grid[self.row + 1][self.col]] = 1

		# if self.row > 0:
		# 	# UP
		# 	if grid[self.row - 1][self.col].is_barrier() or grid[self.row - 1][self.col].is_object():
		# 		self.neighbors[grid[self.row - 1][self.col]] = float("inf")
		# 	else:
		# 		self.neighbors[grid[self.row - 1][self.col]] = 1				

		# if self.col < self.total_rows - 1:
		# 	if grid[self.row][self.col + 1].is_barrier() or grid[self.row][self.col + 1].is_object(): # RIGHT
		# 		self.neighbors[grid[self.row][self.col + 1]] = float("inf")
		# 	else:
		# 		self.neighbors[grid[self.row][self.col + 1]] = 1

		# if self.col > 0:
		# 	if grid[self.row][self.col - 1].is_barrier() or grid[self.row][self.col - 1].is_object(): # LEFT
		# 		self.neighbors[grid[self.row][self.col - 1]] = float("inf")
		# 	else:
		# 		self.neighbors[grid[self.row][self.col - 1]] = 1
		

	def __lt__(self, other):
		return False







# def make_grid(rows, start_coord, end_coord, width):
# 	grid = []
# 	gap = width // rows
# 	start_x, start_y = start_coord
# 	end_x, end_y = end_coord
# 	# gap = (end_row - start_row) // rows
# 	print(start_x,start_y)
# 	print(end_x, end_y)
# 	print(gap)
# 	for i in range(rows):
# 		grid.append([])
# 		for j in range(rows):
# 			spot = Spot(i, j, gap, rows, (start_x, start_y, end_x, end_y))
# 			grid[i].append(spot)

# 	return grid

# def draw_grid(win, rows, start_coord, end_coord, width):
# 	gap = width // rows
# 	start_x, start_y = start_coord
# 	end_x, end_y = end_coord

# 	# # X lines (horizontal)
# 	# for i in range(rows):
# 	# 	pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
# 	# 	print((0, i * gap), (width, i * gap))
# 	# #Y lines (vertical)
# 	# for j in range(rows):
# 	# 	pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# 	for i in range(rows):
# 		# print(f"H line {i}")
# 		pygame.draw.line(win, GREY, (start_x, start_y + (i * gap)), (end_x, start_y + (i * gap)))
# 	#Y lines (vertical)
# 	for j in range(rows):	
# 		pygame.draw.line(win, GREY, (start_x + (j * gap), start_y), (start_x + (j * gap), end_y))

def reverse_path(path, current):
	end = current
	path_list = []
	reverse = {}
	while current in path:
		current = path[current]
		path_list.append(current)
	path_list.reverse()

	for pos in range(len(path_list)-1):
		reverse[path_list[pos]] = path_list[pos+1]

	reverse[path_list[len(path_list)-1]] = end

	return reverse	

def draw(win, mode, alg, grid_list, top_menu, rows, width):

	win.fill(WHITE)
	# if mode == "DESIGN":
	design_grid = grid_list[0]
	grid = design_grid.get_grid()
	for row in grid:
		for spot in row:
			spot.draw(win)
	
	design_grid.draw_grid(win)

	top_menu.update_mode(win, mode)	
	top_menu.update_alg(win, alg)
	pygame.display.update()


def get_clicked_spot_grid(pos, grids):

	x, y = pos
	clicked_grid = None
	for grid in grids:
		print(x,y)
		print(grid.start_x, grid.end_x, grid.start_y, grid.end_y)
		if (grid.start_x <= x <= grid.end_x) and (grid.start_y <= y <= grid.end_y):
			print("grid found!" )
			clicked_grid = grid
			break
	
	if clicked_grid:	
		spot = clicked_grid.get_spot(x=x, y=y)	

	return spot
	# row = y // gap
	# col = x // gap
	# return row, col


def main(win, win_size, top_menu_height):

	ROWS = 50
	start = None
	end = None
	planned_path = None
	current = None
	# d*
	k_m = 0
	queue = []
	g_score = {}
	rhs_score = {}
	mode = "DESIGN"
	alg = "NONE"
	width, height = win_size	
	
	# in design mode start with only one grid
	start_coord_grid = (0, top_menu_height)
	end_coord_grid = (width, height)
	grid_width = width
	# Make design grid
	design_grid = Grid(ROWS, grid_width, start_coord_grid, end_coord_grid)	
	design_grid.make_grid()
	grids = [design_grid]

	top_menu = top_menu = TopBar(0, 0, width, top_menu_height)

	run = True
	while run:
		draw(win, mode, alg, grids, top_menu, ROWS, width)
		if mode == "DESIGN":			
			# run = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = pygame.mouse.get_pos()
					# row, col = get_clicked_pos(pos, ROWS, width)
					# spot = grid.get_spot(row,col)
					spot = get_clicked_spot_grid(pos, grids)
					if not start and spot != end:
						start = spot
						start.make_start()

					elif not end and spot != start:
						end = spot
						end.make_end()

					elif spot != end and spot != start:
						spot.make_barrier()

				elif pygame.mouse.get_pressed()[2]: # RIGHT
					pos = pygame.mouse.get_pos()
					# row, col = get_clicked_pos(pos, ROWS, width)
					# spot = grid.get_spot(row,col)
					spot = get_clicked_spot_grid(pos, grids)
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None

				if event.type == pygame.KEYDOWN:					
					if event.key == pygame.K_SPACE and start and end:
						upd_grid = grids[0].get_grid()
						for row in upd_grid:
							for spot in row:
								spot.update_neighbors(upd_grid)						
						mode = "EXECUTION"
						alg = "a-star"

					if event.key == pygame.K_RETURN and start and end:
						upd_grid = grids[0].get_grid()
						for row in upd_grid:
							for spot in row:
								spot.update_neighbors(upd_grid)		
						mode = "EXECUTION"
						alg = "d-star-lite"

					if event.key == pygame.K_c:
						start = None
						end = None
						planned_path = None
						current = None
						mode = "DESIGN"
						grids[0].reset_grid()
						# grid = make_grid(ROWS, width)
		if mode == "EXECUTION":
			if alg == "a-star":
				planned_path = a_star(lambda: draw(win, mode, alg, grids, top_menu, ROWS, width), upd_grid, start, end)
				# make path from start to end
				planned_path = reverse_path(planned_path, end)
				print("alg execution ended! ")
				mode = "WALK"
				end.make_end()
				current = start
			elif alg == "d-star-lite":
				# d_star_lite
				last = start
				current = start
				print("running D*")
				queue, k_m = d_star_lite(lambda: draw(win, mode, alg, grids, top_menu, ROWS, width), upd_grid, queue, start, end, k_m)
				print("FINISHED running D*")
				mode = "WALK"
				start.make_start()
				end.make_end()


		if mode == "WALK":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				#place an object
				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = pygame.mouse.get_pos()					
					spot = get_clicked_spot_grid(pos, grids)
					# if any point except for start, end or barrier
					if spot != end and spot != start and not spot.is_barrier() and not spot.is_path():
						spot.make_object()
						upd_grid = grids[0].get_grid()
						for row in upd_grid:
							for spot in row:
								spot.update_neighbors(upd_grid)	

				# undo object placement
				elif pygame.mouse.get_pressed()[2]: # RIGHT
					pos = pygame.mouse.get_pos()
					spot = get_clicked_spot_grid(pos, grids)
					if spot.is_object():
						spot.reset()					

				if event.type == pygame.KEYDOWN:					
					if event.key == pygame.K_SPACE and planned_path:						
						next = planned_path[current]
						if next != end:
							# hit an object
							if next.is_object():
								## behaviour for a*								
								start, current = current, start
								start.make_start()
								current.reset()							
								current = None
								planned_path = None
								# now done at every object placement
								grids[0].reset_search_area()
								upd_grid = grids[0].get_grid()
								for row in upd_grid:
									for spot in row:
										spot.update_neighbors(upd_grid)						
								mode = "EXECUTION"
							else:
								current = next
								current.make_path()
					
					if event.key == pygame.K_RETURN:
						print(f"current position {current.get_pos()} ")
						next, k_m = move_and_rescan(lambda: draw(win, mode, alg, grids, top_menu, ROWS, width), queue, current, end, SCAN_RANGE, k_m)
						print(f"next position {next.get_pos()} ")
						current = next
						current.make_path()
						

					if event.key == pygame.K_c:
						start = None
						end = None
						planned_path = None
						current = None
						mode = "DESIGN"
						grids[0].reset_grid()
					

	pygame.quit()

main(WIN, (WIN_WIDTH, WIN_HEIGHT), int(WIN_WIDTH * (TOP_MENU_HEIGHT)))