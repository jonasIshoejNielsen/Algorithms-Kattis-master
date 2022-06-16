from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

class Edge(object):
    def __init__(self, fromN, toN, capacity):
        self.fromN = fromN
        self.toN = toN
        self.capacity = capacity
        
    def toString (self):
        return str(self.fromN.value) + "  -"+str(self.capacity)+"-  "+str(self.toN.value)
    
    def decreaseCapacityBy(self, b):
        self.capacity -=b
        reverseEdge = self.toN.findEdgeTo(self.fromN)
        if reverseEdge is not None:
            reverseEdge.capacity += b
        else:
            self.toN.edges.append(Edge(self.toN, self.fromN, b))
        if self.capacity<=0:
            self.fromN.edges.remove(self)
        
    def __lt__(self, other):
        return -self.capacity < -other.capacity
    def correct(self):
        return self.capacity == 1
    
class Node(object):
    def __init__(self, value):
        self.edges = []
        self.value = value
        self.originalEdges = []
    
    def setEdgesTo(self, nodes, capacity):
        self.edges = [Edge(self, node, capacity) for node in nodes]
    def addEdgeTo(self, node, capacity):
        self.edges.append(Edge(self, node, capacity))
    def findEdgeTo(self, node):
        for e in self.edges:
            if e.toN == node:
                return e
        return None
        
    def getOriginalNonExistingEdge(self):
        for e in self.originalEdges:
            if e in self.edges:
                continue
            return e
        return None
    
    def flowOut(self):
        sum = 0
        for e in self.edges:
            sum += e.capacity
        return sum
    def printSelf(self):
        print(self.value)
        for e in self.edges:
            print("    " + e.toString())
    def correct(self):
        for e in self.edges:
            if not e.correct():
                return False
        return True

class Case(object):
    def __init__(self):
        self.t          = Node("t")
        self.s          = Node("s")
        self.gophers    = []
        self.gopherHoleEdges = 0
        self.holes      = []

    def addGophers(self, x, y):
        node = Node((x, y, "g"))
        self.gophers.append(node)
        self.s.addEdgeTo(node, 1)
        self.s.originalEdges.append(self.s.edges[-1])

    def addHole(self, x, y, distOneCanRun):
        node = Node((x, y, "h"))
        self.holes.append(node)
        node.addEdgeTo(self.t, 1)
        node.originalEdges.append(node.edges[-1])
        for g in self.gophers:
            distance2 = round((g.value[0]-x)**2 + (g.value[1]-y)**2,3)     
            if distance2 <= distOneCanRun:
                g.addEdgeTo(node, 1)
                g.originalEdges.append(g.edges[-1])
                self.gopherHoleEdges +=1
    
    def printCase(self):
        self.s.printSelf()
        self.t.printSelf()
        for e in self.gophers:
            e.printSelf()
        for e in self.holes:
            e.printSelf()
    
    def correct(self):
        if not self.t.correct(): return False
        if not self.s.correct(): return False
        for n in self.gophers: 
            if not n.correct(): return False
        for n in self.holes: 
            if not n.correct(): return False
        return True

def parse_start():
    cases = []
    nrOfEdges, nrOfEdges, distOneCanRun = 0, 0, 0
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.rstrip('\r\n').split(" ")
        if(nrOfEdges==0):
            case = Case()
            cases.append(case)
            nrOfGophers = int(split[0])
            nrOfEdges = int(split[1])
            distOneCanRun = (int(split[2])*int(split[3]) )**2                    #d^2 > ...
            continue
        if nrOfGophers >0:
            case.addGophers(float(split[0]), float(split[1]))
            nrOfGophers -=1
            continue
        case.addHole(float(split[0]), float(split[1]), distOneCanRun)
        nrOfEdges-=1
    return cases


def printPath(lst):
    print("Path:")
    for e in lst:
        print("    " + e.toString())

def findPath(s,t):
    dir = {}
    frontier = []
    for e in s.edges:
        heappush(frontier, e)
    while(frontier != []):
        curr = heappop(frontier)
        if curr.toN in dir:
            continue
        dir[curr.toN] = curr
        for e in curr.toN.edges:
            heappush(frontier, e)
        if t in dir:
            lst = []
            curr = t
            while(curr != s):
                lst.append(dir[curr])
                curr = dir[curr].fromN
            lst.reverse()
            return lst
    return None
def findBottleNeck(lst):
    bottleneck = None
    for e in lst:
        if bottleneck is None:
            bottleneck = e.capacity
        else:
            bottleneck = min(bottleneck, e.capacity)
    return bottleneck

def augment(path):
    bottleneck = findBottleNeck(path)
    for e in path:
        e.decreaseCapacityBy(bottleneck)

def maxFlow(case):
    path = findPath(case.s, case.t)
    
    while (path is not None):
        augment(path)
        if not case.correct():
            raise Exception("not correct")
        path = findPath(case.s, case.t)


cases = parse_start()
for case in cases:
    #case.printCase()
    maxFlow(case)
    print(len(case.gophers) - case.t.flowOut())
