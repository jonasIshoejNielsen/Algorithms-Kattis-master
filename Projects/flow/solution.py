from sys import stdin
from heapq import heappop, heappush

class Node(object):
    def __init__(self, id):
        self.id = id
        self.edges = []

    def set_edge(self, e):
        self.edges.append(e)

    def __str__(self):
        return f"{self.id}"

class Edge(object):
    def __init__(self, u, v, c):
        self.source = u
        self.destination = v
        self.capacity = c if c != -1 else float('inf')
        self.reverse = None

    def decrease_capacity(self, a):
        self.capacity -= a
        self.reverse.capacity += a

    def __lt__(self, other):
        """
        Infix overload of less than operator between edges
        """
        return -self.capacity < -other.capacity

    def __str__(self):
        return f"{self.source} {self.destination} {int(self.reverse.capacity / 2)}"

class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.source = nodes[0]
        self.sink = nodes[-1]

def parse():
    n, nodes = None, None
    for line_number, line in enumerate(stdin):
        if line_number == 0:
            n = int(line)
            nodes = [Node(i) for i in range(n)]
            continue
        if line_number <= n+1:
            continue
        
        u, v, c = [int(x) for x in line.rsplit()]
        e1 = Edge(nodes[u], nodes[v], c)
        e2 = Edge(nodes[v], nodes[u], c)
        e1.reverse, e2.reverse = e2, e1
        nodes[u].set_edge(e1)
        nodes[v].set_edge(e2)
    return Graph(nodes)

def st_path(G):
    s, t = G.source, G.sink
    explored = {}
    frontier = []
    for e in s.edges:
        heappush(frontier, e)
    while(frontier != []):
        curr = heappop(frontier)
        if curr.capacity == 0: continue
        if curr.destination in explored:
            continue
        explored[curr.destination] = curr
        for e in curr.destination.edges:
            heappush(frontier, e)
        if t in explored:
            lst = []
            curr = t
            while(curr != s):
                lst.append(explored[curr])
                curr = explored[curr].source
            lst.reverse()
            return lst, False # False means "not done" with FF
    return explored, True # True means "done" with FF

def bottleneck(path):
    bottleneck = None
    for e in path:
        if bottleneck is None:
            bottleneck = e.capacity
        else:
            bottleneck = min(bottleneck, e.capacity)
    return bottleneck

def augment(path):
    b = bottleneck(path)
    for e in path:
        e.decrease_capacity(b)

def max_flow(G):
    explored, is_done = st_path(G)
    while is_done is False:
        augment(explored)
        explored, is_done = st_path(G)
    return min_cut(explored)

def min_cut(explored):
    cut = []
    for node in explored:
        for e in node.edges:
            if e.destination not in explored:
                cut.append(e)
    return cut

def print_cut(cut):
    # Only sorting to make your diff clean, dear TA :-)
    cut = sorted(cut, key=lambda e: e.source.id)
    sum = 0
    for e in cut:
        print(e)
        sum += int(e.reverse.capacity / 2)
    print("Flow = "+str(sum))

G = parse()
cut = max_flow(G)
print_cut(cut)
