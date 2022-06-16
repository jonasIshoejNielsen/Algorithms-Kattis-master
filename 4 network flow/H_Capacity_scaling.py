from sys import stdin
from heapq import heappop, heappush
import math

class Edge(object):
    def __init__(self, fromN, toN, c):
        self.toN        = toN
        self.fromN      = fromN
        self.capacity   = c
        self.flow       = 0
        self.reverse    = None

    def decrease_capacity(self, a):
        self.flow           += a
        self.reverse.flow   -= a
        self.capacity -= a
        self.reverse.capacity += a

    def __lt__(self, other):
        return -self.capacity < -other.capacity

    def __str__(self):
        return f"     {self.fromN}  -{self.capacity}-  {self.toN}"

class Node(object):
    def __init__(self, id):
        self.id = id
        self.edges = []
        
    def add_edge(self, e):
        self.edges.append(e)
        
    def findEdgeTo(self, node):
        for e in self.edges:
            if e.toN == node:
                return e
        return None
    
    def flowIn(self):
        sum = 0
        for e in self.edges:
            sum += e.reverse.flow
        return sum
    
    def __str__(self):
        return f"{self.id}"
    
    def printDetailed(self):
        print(self)
        for e in self.edges:
            print(e)
            
class Case(object):
    def __init__(self, numberOfNodes, sIndex, tIndex):
        self.nodes  = [Node(i) for i in range(numberOfNodes)]
        self.s      = self.nodes[sIndex]
        self.t      = self.nodes[tIndex]
        self.delta = 0
        
    def createEdges(self, u, v, c):
        existingEdge = self.nodes[u].findEdgeTo(self.nodes[v])
        self.delta = max(c,self.delta)
        if existingEdge is None:
            e1 = Edge(self.nodes[u], self.nodes[v], c)
            e2 = Edge(self.nodes[v], self.nodes[u], 0)
            e1.reverse, e2.reverse = e2, e1
            self.nodes[u].add_edge(e1)
            self.nodes[v].add_edge(e2)
        else:
            existingEdge.capacity += c
            #existingEdge.reverse.capacity += c
    
    def divideCapacity(self):
        if self.delta == 1:
            self.delta = None
        else:
            self.delta = math.floor(self.delta/2)
    
    
    def printCase(self):
        self.s.printDetailed()
        self.t.printDetailed()
        for n in self.nodes:
            n.printDetailed()      
        


def parse_start():
    case = None
    for line_number, line in enumerate(stdin):
        split = line.rstrip('\r\n').split(" ")
        if line_number == 0:
            case = Case(int(split[0]), int(split[2]), int(split[3]))
            continue
        case.createEdges(int(split[0]),int(split[1]),int(split[2]))
    case.divideCapacity()
    return case





def st_path(s,t, delta):
    visitedNodes = {}
    frontier     = []
    for e in s.edges:
        heappush(frontier, (-e.capacity,e))
    while(frontier != []):
        popped = heappop(frontier)
        curr = popped[1]
        if curr.capacity <= 0: continue     #todo test if should be ==0
        if curr.capacity < delta: continue
        if curr.toN in visitedNodes:
            continue
        visitedNodes[curr.toN] = curr
        for e in curr.toN.edges:
            heappush(frontier, (max(popped[0],-e.capacity), e))
        if t in visitedNodes:
            lst = []
            curr = t
            while(curr != s):
                lst.append(visitedNodes[curr])
                curr = visitedNodes[curr].fromN
            lst.reverse()
            return lst
    return None

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

def max_flow(case):
    while case.delta is not None:
        path = st_path(case.s, case.t, case.delta)
        while path is not None:
            augment(path)
            path = st_path(case.s, case.t, case.delta)
        case.divideCapacity()

def printPath(lst):
    if lst is None:
        print("    None")
    else:
        for e in lst:
            print(e)

case = parse_start()
max_flow(case)

edgesWithFlow = []
n = len(case.nodes)
f = case.t.flowIn()
mLines = []

for node in case.nodes:
    for e in node.edges:
        if e.flow <= 0:
            continue
        mLines.append(str(e.fromN.id)+" " + str(e.toN.id) + " "+str(e.flow))

print(n,f,len(mLines))
for m in mLines:
    print(m)