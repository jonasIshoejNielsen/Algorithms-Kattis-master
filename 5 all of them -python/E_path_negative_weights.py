from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *
#Single source shortest path, negative weights
#Bellan ford algorithm
class Edge(object):
    def __init__(self, fromN, toN, cost):
        self.fromN  = fromN
        self.toN    = toN
        self.cost   = cost
        
      
    def __lt__(self, other):
        return self.cost < other.cost
        
    def toString (self):
        return str(self.fromN.value) + "  -"+str(self.cost)+"-  "+str(self.toN.value)
        
    
class Node(object):
    def __init__(self, value):
        self.edges = []
        self.value = value
    
    def findEdgeTo(self, node):
        for e in self.edges:
            if e.toN == node:
                return e
        return None
    
    def addEdgeTo(self, node, cost):
        existingEdge = self.findEdgeTo(node)
        if existingEdge is None:        
            edge = Edge(self, node, cost)
            self.edges.append(edge)
            return edge
        else:
            existingEdge.cost = min(existingEdge.cost, cost)
            return None
    
    def checkOnlyOneConnectingEach(self):
        visited = set([])
        for e in self.edges:
            if e.toN.value in visited:
                print("error-multiple with same ending")
                break
            visited.add(e.toN.value)
        
    def printSelf(self):
        print(self.value)
        for e in self.edges:
            print("    " + e.toString())

class Case(object):
    def __init__(self, numberOfNodes, sIndex):
        self.nodes      = [Node(i) for i in range(numberOfNodes)]     #ignore nodes[0]
        self.queries    = []
        self.s          = self.nodes[sIndex]
        self.edges      = []

    def addEdgeFromTo(self, start, end, cost):
        node = self.nodes[end]
        edge = self.nodes[start].addEdgeTo(node, cost)
        if edge is not None:
            self.edges.append(edge)
    def checkOnlyOneConnectingEach(self):
        for n in self.nodes:
            n.checkOnlyOneConnectingEach()
            
    def printCase(self):
        print("S:")
        self.s.printSelf()
        for t in self.queries:
            print("T:")
            t[1].printSelf()
        for n in self.nodes:
            n.printSelf()

def parse_start():
    cases = []
    case = None
    numberOfEdges = 0
    numberOfQueries = 0
    for (line_number, line) in enumerate(stdin):
        split = line.rstrip('\r\n').split(" ")
        if(numberOfEdges==0 and numberOfQueries==0):
            notdone = False
            for i in split: notdone = notdone or i!="0"
            if not notdone: break
            
            case = Case(int(split[0]), int(split[3]))
            cases.append(case)
            numberOfEdges   = int(split[1])
            numberOfQueries = int(split[2])
            continue
        if numberOfEdges>0:
            case.addEdgeFromTo(int(split[0]), int(split[1]), int(split[2]))
            numberOfEdges-=1
            continue
        case.queries.append((int(split[0]), case.nodes[int(split[0])]))
        numberOfQueries-=1
    return cases

def RemoveIfThere(set, item):
    if item in set:
        set.discard(item)

def findPath(case, s):   #https://www.youtube.com/watch?v=FtN3BYH2Zes&ab_channel=AbdulBari
    n = len(case.nodes)
    v = len(case.edges)
    M = [float('inf') for _ in range(n)]
    M[s] = 0
    for i in range(n-1):
        for e in case.edges:        #(u,v)
            u = e.fromN.value
            v = e.toN.value
            M[v] = min(M[u] + e.cost, M[v])
    M2 = M.copy()
    for i in range(n-1):
        for e in case.edges:        #(u,v)
            u = e.fromN.value
            v = e.toN.value
            if M2[u] + e.cost < M2[v]:
                M2[v] = - float('inf')
    return M,M2            
 

def dijkstra(s):
    dir = {}
    frontier = []
    setOfQueries = set([ q for i,q in case.queries])
    dir[s] = (0, None)
    RemoveIfThere(setOfQueries, s)
    
    for e in s.edges:
        heappush(frontier, (0, e))
    while(frontier != [] and len(setOfQueries)!=0):
        (t, curr) = heappop(frontier)
        nextT = t + curr.cost
        if curr.toN in dir:
            (t2, curr2) = dir[curr.toN]
            if t2 <= nextT:
                continue
        dir[curr.toN] = (nextT, curr)
        for e in curr.toN.edges:
            heappush(frontier, (nextT, e))
    return dir   
    
def nonShortestPath(s):
    dir = {}
    frontier = []
    setOfQueries = set([ q for i,q in case.queries])
    dir[s] = (0, None)
    RemoveIfThere(setOfQueries, s)
    
    for e in s.edges:
        heappush(frontier, (0, e))
    while(frontier != [] and len(setOfQueries)!=0):
        (t, curr) = heappop(frontier)
        nextT = t + curr.cost
        if curr.toN in dir:
            continue
        dir[curr.toN] = (nextT, curr)
        for e in curr.toN.edges:
            heappush(frontier, (nextT, e))
    return dir 

def printPath(path):
    print("Path")
    for k in path:
        (t,e) = path[k]
        if e is None: print("   "+str(t)+" : None")
        else:         print("   "+str(t)+" : "+e.toString())

cases = parse_start()
first = True
for case in cases:
    if first:   first = False
    else:       print("")
    M,M2 = findPath(case, case.s.value)
    #case.checkOnlyOneConnectingEach()
    for q in case.queries:
        if M[q[0]] != M2[q[0]]:
            print("-Infinity")
        elif M[q[0]] == float('inf'):
            print("Impossible")
        else: print(M[q[0]])
    """
    #test dijkstra      #set minCost to 0
    dijk = dijkstra(case.s)
    for q in case.queries:
        if q[1] in dijk:
            (t,e) = dijk[q[1]]
            if t!= M[q[0]]:
                print("error1")
        else:
            if M[q[0]] != float('inf'):
                print("Error Impossible", )"""
    
    
    """
    #test reachable
    reachables = nonShortestPath(case.s)
    for q in case.queries:
        if q[1] in reachables:
            (t,e) = reachables[q[1]]
            if M[q[0]] == float('inf'):
                print("error1")
        else:
            if M[q[0]] != float('inf'):
                print("Error Impossible", )
    """