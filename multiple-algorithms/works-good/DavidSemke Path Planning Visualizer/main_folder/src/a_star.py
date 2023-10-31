import min_heap as heap
from search_tools import *

def a_star_shortest_path(
        draw_func, start, end, g_dict, f_dict, open_set
):
    global PERCOLATES
    global EXPANSIONS
    global ACCESSES
    global COUNT

    while open_set:  # heap is not empty
        item, percolates = heap.heappop(open_set)
        current = item[2]
        PERCOLATES += percolates

        if current is end: return True

        for neighbor in current.neighbors:
            temp_g_score = g_dict[current] + EDGE_COST
            ACCESSES += 2

            if temp_g_score >= g_dict[neighbor]: continue
            
            ACCESSES += 2
            g_dict[neighbor] = temp_g_score
            h = heuristic(neighbor.get_pos(), end.get_pos())
            f_dict[neighbor] = temp_g_score + h

            neighbor_in_heap = any(
                neighbor is item[2] for item in open_set
            )

            if neighbor_in_heap: continue
            
            ACCESSES += 1
            PERCOLATES += heap.heappush(
                open_set, (f_dict[neighbor], COUNT, neighbor)
            )
            COUNT += 1
            
            if not (
                neighbor.is_invis_barrier() 
                or neighbor.is_path() 
                or neighbor.is_start()
            ):
                neighbor.make_open()

        draw_func()

        if not (
            current is start 
            or current.is_invis_barrier() 
            or current.is_path()
        ):
            current.make_closed()

        EXPANSIONS += 1

    return False


def a_star(draw_func, env, travel):
    global PERCOLATES
    global EXPANSIONS
    global ACCESSES
    global COUNT
    PERCOLATES = 0
    EXPANSIONS = 0
    ACCESSES = 0
    COUNT = 0

    g_dict = {node: float("inf") for row in env['grid'] for node in row}
    f_dict = {node: float("inf") for row in env['grid'] for node in row}

    # if travel true, the agent will attempt to move from start to 
    # goal position; else, the shortest path is computed
    if travel:
        a_star_with_travel(draw_func, env, g_dict, f_dict)
    
    else:
        a_star_without_travel(draw_func, env, g_dict, f_dict)

    print("Heap percolates: " + str(PERCOLATES))
    print("Node expansions: " + str(EXPANSIONS))
    print("Node accesses: " + str(ACCESSES))


# compute shortest path with A*, and traverse to goal position
def a_star_with_travel(draw_func, env, g_dict, f_dict):
    global PERCOLATES
    global ACCESSES
    global COUNT

    grid = env['grid']
    start = env['start']
    end = env['end']

    origin = start

    ACCESSES += 2
    g_dict[end] = 0
    f_dict[end] = heuristic(start.get_pos(), end.get_pos())

    open_set_heap = [(0, COUNT, end)]
    COUNT += 1

    # make all invis barriers within range of agent's vision at start 
    # position vis
    for n in origin.neighbors:
        
        if not n.is_invis_barrier(): continue
        
        n.make_vis_barrier()
        
        for n_neighbor in n.neighbors:
            n_neighbor.update_neighbors(grid)
    
    SUCCESS = "Journey completed via A* (with travel)."
    FAIL = "A* (with travel) failed to find path to goal."

    path_exists = a_star_shortest_path(
        draw_func, end, start, g_dict, f_dict, open_set_heap
    )

    if not path_exists:
        print(FAIL)
        return
        
    while start is not end:
        next_start_node = None
        min_dist = float("inf")
        
        for n in start.neighbors:
            ACCESSES += 1
            poss_new_min_dist = g_dict[n]
            
            if poss_new_min_dist < min_dist:
                min_dist = poss_new_min_dist
                next_start_node = n

        start.make_path()
        start = next_start_node
        start.make_start()

        draw_func()

        # the next step simulates scanning for changes in edge 
        # costs
        # changes to graph can occur one node away from the start 
        # node in any direction
        nodes_changed = []
        
        for n in start.neighbors:
            
            if not n.is_invis_barrier(): continue
            
            n.make_vis_barrier()
            nodes_changed.append(n)
            
            # remove from heap if present
            for i, item in enumerate(open_set_heap):
                
                if n is not item[2]: continue
                
                PERCOLATES += heap.heapremove(open_set_heap, i)
                
                break

        if not nodes_changed: continue
            
        # note that some code has been omitted here, as the 
        # code would not apply to an environment with
        # solely traversable and not traversable edges (edge 
        # is either some constant or infinity)
        for n in nodes_changed:
            n.update_neighbors(grid)
            
            for n_neighbor in n.neighbors:
                n_neighbor.update_neighbors(grid)

        # reset everything and start search fresh
        for row in grid:
            for node in row:

                if not (
                    node.is_closed() 
                    or node.is_open() 
                    or node.is_path() 
                    or node.is_start() 
                    or node.is_end()
                    or node.is_invis_barrier()
                ):
                    continue
                    
                if node.is_open() or node.is_closed():
                    node.reset()
                
                ACCESSES += 2
                g_dict[node] = float("inf")
                f_dict[node] = float("inf")

        COUNT = 0
        open_set_heap = [(0, COUNT, end)]
        COUNT += 1
        g_dict[end] = 0
        f_dict[end] = heuristic(start.get_pos(), end.get_pos())
        ACCESSES += 2

        path_exists = a_star_shortest_path(
            draw_func, end, start, g_dict, f_dict, open_set_heap
        )

        if not path_exists: break

    if start is end:
        origin.make_original_start()
        print(SUCCESS)
    
    else:
        print(FAIL)
        


# compute shortest path with A*, and adapt path to changes if they 
# occur (without traversing to goal)
def a_star_without_travel(draw_func, env, g_dict, f_dict):
    global PERCOLATES
    global ACCESSES
    global COUNT

    ACCESSES += 2

    grid = env['grid']
    start = env['start']
    end = env['end']
    invis_barriers = env['invis_barriers']

    g_dict[start] = 0
    f_dict[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_heap = [(0, COUNT, start)]
    COUNT += 1

    if a_star_shortest_path(
        draw_func, start, end, g_dict, f_dict, open_set_heap
    ):
        reconstruct_path(start, end, g_dict, draw_func)
        end.make_end()
        start.make_start()

        draw_func()

    for b in invis_barriers:
        b.make_vis_barrier()
        
        for i, item in enumerate(open_set_heap):
            
            if not b is item[2]: continue
            
            PERCOLATES += heap.heapremove(open_set_heap, i)
            
            break

        b.update_neighbors(grid)

        for b_neighbor in b.neighbors:
            b_neighbor.update_neighbors(grid)

        # clear previous activity
        for row in grid:
            for node in row:

                if not (
                    node.is_path() 
                    or node.is_closed() 
                    or node.is_open() 
                    or node.is_start() 
                    or node.is_end()
                    or node.is_invis_barrier()
                ):
                    continue
                
                if (
                    node.is_closed() 
                    or node.is_open() 
                    or node.is_path()
                ):
                    node.reset()

                ACCESSES += 2
                g_dict[node] = float("inf")
                f_dict[node] = float("inf")

        COUNT = 0
        open_set_heap = [(0, COUNT, start)]
        COUNT += 1
        g_dict[start] = 0
        f_dict[start] = heuristic(start.get_pos(), end.get_pos())

        ACCESSES += 2

        path_exists = a_star_shortest_path(
            draw_func, start, end, g_dict, f_dict, open_set_heap
        )

        if not path_exists: continue
        
        reconstruct_path(start, end, g_dict, draw_func)
        end.make_end()
        start.make_start()
        draw_func()

    print("A* (without travel) completed trials.")