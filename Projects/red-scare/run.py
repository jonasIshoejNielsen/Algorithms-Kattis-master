import sys
sys.setrecursionlimit(2500000)

from Parser import parse
from Graph import Graph, Node
from Pathfinding import bfs, dfs, dijkstra, bellman_ford
from Flow import max_flow, construct_flow_graph, reset_flow_graph

def none(G):
    p = bfs(G, lambda x, y: not y.is_red or y == G.t)
    return -1 if p is None else len(p)

def many(G):
    if not G.is_directed:
        return "-"      #cycles stop us
    t_value = bellman_ford(G)
    if t_value == - float("inf"):
        return "-"      #cycles stop us
    if t_value == float("inf"):
        return -1
    return abs(t_value)

def few(G):
    p = dijkstra(G, lambda x, y: 1 if y.is_red else 0)
    return -1 if p is None else len([x for x in p if x.is_red])

def alternating(G):
    p = bfs(G, lambda x, y: x.is_red != y.is_red)
    return p != None

def some(G: Graph):
    if G.s.is_red or G.t.is_red:
        p = bfs(G, lambda x, y:True)
        return p is not None
    if G.is_directed:
        val = many(G)
        if type(val) != str:
            if val == -1:
                return False
            return val > 0
        return val        
        
    for node in G.nodes:
        if not node.is_red: continue
        G = construct_flow_graph(G, node)
        if max_flow(G) == 2: return True
        G = reset_flow_graph(G)
    return False

G = parse()
"""
print("Alternating:", alternating(G))
print("Few:", few(G))
print("Many:", many(G))
print("None:", none(G))
print("Some:", some(G))"""

print(*["",len(G.nodes), alternating(G), few(G), many(G), none(G), some(G)], sep=' & ')
