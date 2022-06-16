from sys import stdin
from heapq import heappop, heappush

class Edge(object):
    def __init__(self, fromN, toN, c):
        self.toN        = toN
        self.fromN      = fromN
        self.capacity   = c
        self.flow       = 0
        self.reverse    = None

    def decrease_capacity(self, a):
        self.toN.excess     += a
        self.fromN.excess   -= a
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
        self.height = 0
        self.edges = []
        self.excess = 0
        
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
    
    def relabel(self):
        lowestEdge = None
        for e in self.edges:
            if e.capacity ==0:
                continue
            if e.toN.height < self.height:
                return e
            if lowestEdge is None:
                lowestEdge = e
                continue
            if e.toN.height < lowestEdge.toN.height:
                lowestEdge = e
        self.height = lowestEdge.toN.height + 1
        return lowestEdge
        
    
    
    def __str__(self):
        return f"{self.id}"
    
    def printDetailed(self):
        print(f"{self.id}   H={self.height}   ce={self.excess}")
        for e in self.edges:
            print(e)
            
class Case(object):
    def __init__(self, numberOfNodes, sIndex, tIndex):
        self.nodes  = [Node(i) for i in range(numberOfNodes)]
        self.s      = self.nodes[sIndex]
        self.t      = self.nodes[tIndex]
        self.nodesWithExcess = []
        
    def createEdges(self, u, v, c):
        existingEdge = self.nodes[u].findEdgeTo(self.nodes[v])
        if existingEdge is None:
            e1 = Edge(self.nodes[u], self.nodes[v], c)
            e2 = Edge(self.nodes[v], self.nodes[u], 0)
            e1.reverse, e2.reverse = e2, e1
            self.nodes[u].add_edge(e1)
            self.nodes[v].add_edge(e2)
        else:
            existingEdge.capacity += c
            #existingEdge.reverse.capacity += c
    def finish(self):
        for e in self.s.edges:
            e.decrease_capacity(e.capacity)
            self.nodesWithExcess.append(e.toN)
        self.s.height = len(self.nodes)
            
    def printCase(self):
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
    case.finish()
    return case




def preflow_push(case):
    while len(case.nodesWithExcess) != 0:
        node = case.nodesWithExcess.pop()
        if node.excess == 0:
            continue
        if node == case.s or node == case.t:
            continue
        edge = node.relabel()
        edge.decrease_capacity(min(edge.capacity, node.excess))
        case.nodesWithExcess.append(node)
        case.nodesWithExcess.append(edge.toN)



def reachableNodesFromT(s):
    visitedNodes = {}
    frontier     = []
    visitedNodes[s] = None
    for e in s.edges:
        heappush(frontier, (-e.capacity,e))
    while(frontier != []):
        popped = heappop(frontier)
        curr = popped[1]
        if curr.capacity <= 0: continue     #todo test if should be ==0
        if curr.toN in visitedNodes:
            continue
        visitedNodes[curr.toN] = curr
        for e in curr.toN.edges:
            heappush(frontier, (max(popped[0],-e.capacity), e))
    return visitedNodes


case = parse_start()
preflow_push(case)


edgesWithFlow = []
n = len(case.nodes)
f = case.t.flowIn()
mLines = []

for node in case.nodes:
    for e in node.edges:
        if e.flow <= 0:
            continue
        mLines.append(str(e.fromN.id)+" " + str(e.toN.id) + " "+str(e.flow))

cut = reachableNodesFromT(case.s)
print(len(cut))
for n in reachableNodesFromT(case.s):
    print(n)