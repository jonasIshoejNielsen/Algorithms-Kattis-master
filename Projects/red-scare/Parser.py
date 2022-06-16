from sys import stdin
from Graph import Graph, Node

def parse() -> Graph:
    num_nodes, num_edges, _ = map(int, input().rsplit())
    s_id, t_id = input().rsplit()
    nodes, edges, is_directed = {}, [], True

    for _ in range(num_nodes):
        split = input().rsplit()
        id, is_red = split[0], len(split) == 2
        node = Node(id, is_red)
        nodes[node.id] = node

    for _ in range(num_edges):
        n1, e, n2 = input().rsplit()
        n1, n2 = nodes[n1], nodes[n2]
        n1.set_neighbor(n2)
        edges.append((n1,n2))
        if e == "--":
            is_directed = False
            n2.set_neighbor(n1)
            edges.append((n2,n1))

    s, t = nodes[s_id], nodes[t_id]
    return Graph(s, t, edges, nodes, is_directed)
