

class TurningPointFinder:

    path = None
    count = 0
    turning_points = []

    def __init__(self, path):
        print("initialized")

    def print_path(self, _path):
        TurningPointFinder.path = _path
        print("--------------------------------")
        print(self.path)
        print("++++++++++++++++++++++++++++++++")
        print(TurningPointFinder.path)
        print("--------------------------------")

    def find_turning_points(self, path):
        self.turning_points.clear()
        if self.count is 0:
            self.count = 1
            for node in path:
                node_index = path.index(node)
                if node_index != 0 and node_index != len(path) - 1:
                    prior_node = path[node_index - 1]
                    posterior_node = path[node_index + 1]
                    if prior_node[0] != posterior_node[0] and prior_node[1] != posterior_node[1]:
                        print("This is a turning point and its coordinates are:", node)
                        self.turning_points.append(node)
        print("Length of turning points is", len(self.turning_points))



    # For 8N discovery we should change this code.
    # We should count the turning points.
    # If we find a turning point, then we should get the next
    # index and not check its turning case
    # Because in 8N discovery, we are facing with non-linear movement.
    # This amount should change due to the dimensions of our playground.
