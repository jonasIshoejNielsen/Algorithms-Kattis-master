class Node(object):
    def __init__(self, id: str, is_red: bool):
        self.id = id
        self.is_red = is_red
        self.neighbors: [Node] = []
        self.capacities: {Node: int} = {}
        self.residual_neighbors: [Node] = []
        self.residual_capacities: {Node: int} = {}
        self.value = float('inf')

    def set_neighbor(self, neighbor, capacity=1):
        self.neighbors.append(neighbor)
        self.capacities[neighbor] = capacity

    def capacity_to(self, neighbor):
        capacity = self.capacities.get(neighbor, None)
        if capacity is not None: return capacity
        return self.residual_capacities[neighbor]

    def decrease_capacity_to(self, node, delta: int):
        if self.capacities.get(node, False):
            self.capacities[node] -= delta
            node.decrease_capacity_to(self, -delta)
        if self.residual_capacities.get(node, False):
            self.residual_capacities[node] -= delta
        else:
            self.residual_neighbors.append(node)
            self.residual_capacities[node] = -delta

    def set_capacity_to(self, node, capacity):
        if self.capacities.get(node, False):
            self.capacities[node] = capacity
        else:
            self.residual_capacities[node] = capacity

    def __lt__(self, other):
        return True

class Graph(object):
    def __init__(self, s, t, edges, nodes, is_directed):
        self.s = s
        self.t = t
        self.edges = edges
        self.nodes = [nodes[key] for key in nodes]
        self.is_directed = is_directed
        self.s_id = s.id
        self.t_id = t.id
