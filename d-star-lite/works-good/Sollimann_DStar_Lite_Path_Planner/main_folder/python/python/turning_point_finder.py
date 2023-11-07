

class TurningPointFinder:

    path = None
    count = 0
    turning_points = []

    def __init__(self, path):
        print("initialized")


    def find_turning_points(self, path):
        self.turning_points.clear()
        for node in path:
            node_index = path.index(node)
            if node_index != 0 and node_index != len(path) - 1:
                prior_node = path[node_index - 1]
                posterior_node = path[node_index + 1]
                if prior_node[0] != posterior_node[0] and prior_node[1] != posterior_node[1]:
                    self.turning_points.append(node)

    # For 8N discovery we should change this code.
    # We should count the turning points.
    # If we find a turning point, then we should get the next
    # index and not check its turning case
    # Because in 8N discovery, we are facing with non-linear movement.
    # This amount should change due to the dimensions of our playground.
