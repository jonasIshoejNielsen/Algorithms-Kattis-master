from heapq import heappop, heappush
from Graph import Graph, Node

def construct_flow_graph(G: Graph, red_node: Node) -> Graph:
    for node in G.nodes:
        out_node = Node(node.id + "-out", node.is_red)
        out_node.neighbors = node.neighbors
        out_node.capacities = node.capacities
        node.neighbors = [out_node]
        node.capacities = {out_node: 1}

    super_sink = Node("super_sink", is_red=False)
    s_out, t_out = G.s.neighbors[0], G.t.neighbors[0]
    s_out.set_neighbor(super_sink)
    t_out.set_neighbor(super_sink)
    G.t = super_sink

    super_source = Node("super_source", is_red=False)
    super_source.set_neighbor(red_node, capacity=2)
    red_node_out = red_node.neighbors[0]
    red_node.set_capacity_to(red_node_out, 2)
    G.s = super_source

    return G

def reset_flow_graph(G: Graph) -> Graph:
    for node in G.nodes:
        out_node = node.neighbors[0]
        node.neighbors = out_node.neighbors
        node.residual_neighbors = []
        node.residual_capacities = {}
        node.capacities = {n:1 for n in out_node.neighbors}
    org_s = [s for s in G.nodes if s.id == G.s_id][0]
    org_t = [t for t in G.nodes if t.id == G.t_id][0]
    G.s, G.t = org_s, org_t
    return G

def st_path(G):
    s, t = G.s, G.t
    visited, frontier = {}, []
    for node in s.neighbors + s.residual_neighbors:
        heappush(frontier, (s, node))
    while len(frontier) > 0:
        prev, curr = heappop(frontier)
        if curr in visited: continue
        if prev.capacity_to(curr) == 0: continue
        visited[curr] = prev
        if t in visited:
            path, curr = [t], t
            while(curr != s):
                path.append(visited[curr])
                curr = visited[curr]
            path.reverse()
            return path, False # False means "not done" with FF
        for node in curr.neighbors + curr.residual_neighbors:
            heappush(frontier, (curr, node))
    return visited, True # True means "done" with FF

def bottleneck(path):
    b = float("inf")
    for i in range(len(path) - 1):
        curr_node, next_node = path[i], path[i+1]
        b = min(b, curr_node.capacity_to(next_node))
    return b

def augment(path):
    b = bottleneck(path)
    for i in range(len(path) - 1):
        curr_node, next_node = path[i], path[i+1]
        curr_node.decrease_capacity_to(next_node, b)

def max_flow(G):
    path, is_done = st_path(G)
    while is_done is False:
        augment(path)
        path, is_done = st_path(G)
    value = 0
    for neighbor in G.t.residual_neighbors:
        value += G.t.capacity_to(neighbor)
    return value
