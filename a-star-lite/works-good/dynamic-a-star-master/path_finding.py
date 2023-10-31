import pygame
from queue import PriorityQueue
import heapq
# heuristic function (manhathan)
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def calculate_key(spot, current, k_m):
    k1 = min(spot.g, spot.rhs) + h(spot.get_pos(), current.get_pos()) + k_m
    k2 = min(spot.g, spot.rhs)
    return (k1, k2)

def top_key(queue):
    queue.sort()
    if len(queue) > 0:
        return queue[0][:2]
    else:
        return (float('inf'), float('inf'))    

def update_vertex(draw, queue, spot, current, end, k_m):
    s_goal = end
    if spot != s_goal:
        min_rhs = float('inf')
        for neighbor in spot.neighbors:
            min_rhs = min(min_rhs, neighbor.g + h(spot.get_pos(),neighbor.get_pos()))
        spot.rhs = min_rhs
    id_in_queue = [item for item in queue if spot in item]
    if id_in_queue != []:
        if len(id_in_queue) != 1:
            raise ValueError('more than one spot (' + spot.get_pos() + ') in the queue!')
        queue.remove(id_in_queue[0])
    if spot.rhs != spot.g:
        heapq.heappush(queue, calculate_key(spot, current, k_m) + (spot,))
        spot.make_open()
    draw()

def next_in_shortest_path(current):
    min_rhs = float('inf')
    next = None
    if current.rhs == float('inf'):
        print('You are stuck!')
    else:
        for neighbor in current.neighbors:
            # print(i)
            child_cost = neighbor.g + h(current.get_pos(),neighbor.get_pos())
            # print(child_cost)
            if (child_cost) < min_rhs:
                min_rhs = child_cost
                next = neighbor
        if next:
            return next
        else:
            raise ValueError('No suitable child for transition!')

def scan_obstacles(draw, queue, current, end, scan_range, k_m):
    spots_to_update = []
    range_checked = 0
    if scan_range >= 1:
        for neighbor in current.neighbors:  
            print(f"adding {neighbor.get_pos()} to spots to update")          
            spots_to_update.append(neighbor)
        range_checked = 1
    # print(states_to_update)

    while range_checked < scan_range:
        new_set = []
        for spot in spots_to_update:
            new_set.append(spot)
            print(f"adding {spot.get_pos()} to spots to update")       
            for neighbor in spot.neighbors:
                if neighbor not in new_set:
                    new_set.append(neighbor)
                    print(f"adding {neighbor.get_pos()} to spots to update")       
        range_checked += 1
        spots_to_update = new_set

    #make it unique
    spots_to_update = list(set(spots_to_update))

    new_obstacle = False
    for spot in spots_to_update:
        if spot.is_barrier() or spot.is_object():  # found cell with obstacle
            print('found obstacle in ', spot.get_pos())
            for neighbor in spot.neighbors:
                # first time to observe this obstacle where one wasn't before
                # if(graph.graph[state].children[neighbor] != float('inf')):                    
                update_vertex(draw, queue, spot, current, end, k_m)
                new_obstacle = True
        # elif states_to_update[state] == 0: #cell without obstacle
            # for neighbor in graph.graph[state].children:
                # if(graph.graph[state].children[neighbor] != float('inf')):

    # print(graph)
    return new_obstacle

def move_and_rescan(draw, queue, current, end, scan_range, k_m):
    if(current == end):
        return 'goal', k_m
    else:
        last = current
        new = next_in_shortest_path(current)        

        if(new.is_object() or new.is_barrier()):  # just ran into new obstacle
            print("obstacle")
            new = current  # need to hold tight and scan/replan first

        results = scan_obstacles(draw, queue, new, end, scan_range, k_m)
        # print(graph)
        k_m += h(last.get_pos(), new.get_pos())
        calc_shortest_path(draw, queue, current, end, k_m)

        return new, k_m 

def calc_shortest_path(draw, queue, start, end, k_m):
    while (start.rhs != start.g) or \
          (top_key(queue) < calculate_key(start, start, k_m)):
        # print(graph.graph[s_start])
        # print('topKey')
        # print(topKey(queue))
        # print('calculateKey')
        # print(calculateKey(graph, s_start, 0))
        k_old = top_key(queue)
        u = heapq.heappop(queue)[2]        
        if k_old < calculate_key(u, start, k_m):
            heapq.heappush(queue, calculate_key(u, start, k_m) + (u,))
            u.make_open()
        elif u.g > u.rhs:
            u.g = u.rhs
            for neighbor in u.neighbors:
                update_vertex(draw, queue, neighbor, start, end, k_m)
        else:
            u.g = float('inf')
            update_vertex(draw, queue, u, start, end, k_m)
            for neighbor in u.neighbors:
                update_vertex(draw, queue, neighbor, start, end, k_m)   
        u.make_closed()
        draw()    

def d_star_lite(draw, grid, queue, start, end, k_m):
    #initialization
    # g_score = {spot: float("inf") for row in grid for spot in row}
    # g_score[end] = 0
    # rhs_score = {spot: float("inf") for row in grid for spot in row}
    # rhs_score[end] = 0
    for row in grid:
        for spot in row:
            spot.g = float("inf")
            spot.rhs = float("inf")

    end.g = 0
    end.rhs = 0
    
    heapq.heappush(queue, calculate_key(end, start, k_m) + (end,))
    calc_shortest_path(draw, queue, start, end, k_m)
         
    return queue, k_m


#original implementation from https://morioh.com/p/cf0c6b11c848
def a_star(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			# reconstruct_path(came_from, end, draw)
			# end.make_end()
			return came_from

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		if current != start:
			current.make_closed()
            
		draw()

	return None