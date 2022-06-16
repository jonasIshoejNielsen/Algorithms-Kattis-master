from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *
#Single source shortest path, time table
class Edge(object):
    def __init__(self, fromN, toN, t0, p, cost):
        self.fromN  = fromN
        self.toN    = toN
        self.t0     = t0
        self.p      = p
        self.cost   = cost
        
      
    def __lt__(self, other):
        return self.cost < other.cost
        
    def toString (self):
        return str(self.fromN.value) + "  --  "+str(self.toN.value)
        
    
class Node(object):
    def __init__(self, value):
        self.edges = []
        self.value = value
    
    def addEdgeTo(self, node, t0, p, cost):
        self.edges.append(Edge(self, node, t0, p, cost))
        
    def printSelf(self):
        print(self.value)
        for e in self.edges:
            print("    " + e.toString())

class Case(object):
    def __init__(self, numberOfNodes, sIndex):
        self.nodes      = [Node(i) for i in range(numberOfNodes+1)]     #ignore nodes[0]
        self.queries    = []
        self.s          = self.nodes[sIndex]

    def addEdgeFromTo(self, start, end, t0, p, cost):
        node = self.nodes[end]
        self.nodes[start].addEdgeTo(node, t0, p, cost)
            
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
            case = Case(int(split[0]), int(split[3]))
            cases.append(case)
            numberOfEdges   = int(split[1])
            numberOfQueries = int(split[2])
            continue
        if numberOfEdges>0:
            case.addEdgeFromTo(int(split[0]), int(split[1]), int(split[2]), int(split[3]), int(split[4]))
            numberOfEdges-=1
            continue
        case.queries.append((int(split[0]), case.nodes[int(split[0])]))
        numberOfQueries-=1
    return cases

def RemoveIfThere(set, item):
    if item in set:
        set.discard(item)

def findPath(s):
    dir = {}
    frontier = []
    setOfQueries = set([ q for i,q in case.queries])
    dir[s] = (0, None)      #nextAllowedTime to start, edge to next
    RemoveIfThere(setOfQueries, s)
    
    for e in s.edges:
        heappush(frontier, (0, e))
    while(frontier != [] and len(setOfQueries)!=0):
        (t, curr) = heappop(frontier)
        if t<curr.t0:
            nextAllowedTime = curr.t0 + curr.cost
        elif curr.p==0:
            continue
        else:
            nextAllowedTime =  curr.t0 + curr.p * math.ceil((t-curr.t0)/curr.p) + curr.cost
        
        if curr.toN in dir:
            (t2, curr2) = dir[curr.toN]
            if t2 < nextAllowedTime:
                continue
        
        dir[curr.toN] = (nextAllowedTime, curr)
        #RemoveIfThere(setOfQueries, curr.toN)
        for e in curr.toN.edges:
            heappush(frontier, (nextAllowedTime, e))
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
    path = findPath(case.s)
    for i,q in case.queries:
        if q in path:
            (t,e) = path[q]
            print(t)
        else: print("Impossible")