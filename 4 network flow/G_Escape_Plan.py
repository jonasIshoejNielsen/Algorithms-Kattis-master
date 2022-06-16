from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

class Edge(object):
    def __init__(self, fromN, toN, capacity, dist):
        self.fromN = fromN
        self.toN = toN
        self.capacity = capacity
        self.dist = dist
        
    def toString (self):
        return str(self.fromN.value) + "  -"+str(self.capacity)+"-  "+str(self.toN.value)
    
    def decreaseCapacityBy(self, b):
        self.capacity -=b
        reverseEdge = self.toN.findEdgeTo(self.fromN)
        if reverseEdge is not None:
            reverseEdge.capacity += b
        else:
            self.toN.edges.append(Edge(self.toN, self.fromN, b, self.dist))
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
    
    def setEdgesTo(self, nodes, capacity, dist):
        self.edges = [Edge(self, node, capacity, dist) for node in nodes]
    def addEdgeTo(self, node, capacity, dist):
        self.edges.append(Edge(self, node, capacity, dist))
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
        self.robots    = []
        self.robotHoleEdges = 0
        self.holes      = []

    def addRobot(self, x, y):
        node = Node((x, y, "g"))
        self.robots.append(node)
        self.s.addEdgeTo(node, 1, 0)
        self.s.originalEdges.append(self.s.edges[-1])

    def addHole(self, x, y, distOneCanRun):
        node = Node((x, y, "h"))
        self.holes.append(node)
        node.addEdgeTo(self.t, 1, 0)
        node.originalEdges.append(node.edges[-1])
        for g in self.robots:
            distance2 = round((g.value[0]-x)**2 + (g.value[1]-y)**2,3)     
            if distance2 <= distOneCanRun:
                g.addEdgeTo(node, 1, distance2)
                g.originalEdges.append(g.edges[-1])
                self.robotHoleEdges +=1
    
    def printCase(self):
        self.s.printSelf()
        self.t.printSelf()
        for e in self.robots:
            e.printSelf()
        for e in self.holes:
            e.printSelf()
    
    def correct(self):
        if not self.t.correct(): return False
        if not self.s.correct(): return False
        for n in self.robots: 
            if not n.correct(): return False
        for n in self.holes: 
            if not n.correct(): return False
        return True

def parse_start():
    cases = []
    nrOfRobots, nrOfHoles, distOneCanRun = 0, 0, (10*20)**2
    parseRobots = False
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.rstrip('\r\n').split(" ")
        if(not parseRobots and nrOfRobots==0 and nrOfHoles==0):
            nrOfRobots = int(split[0])
            if nrOfRobots == 0:
                break
            case = Case()
            cases.append(case)
            parseRobots = True
            continue
        if nrOfRobots >0:
            case.addRobot(float(split[0]), float(split[1]))
            nrOfRobots -=1
            continue
        if nrOfHoles == 0:
            parseRobots = False
            nrOfHoles = int(split[0])
            continue
        case.addHole(float(split[0]), float(split[1]), distOneCanRun)
        nrOfHoles-=1
    return cases


def printPath(lst):
    print("Path:")
    for e in lst:
        print("    " + e.toString())

def findPath(s,t, dists):
    dir = {}
    frontier = []
    for e in s.edges:
        heappush(frontier, e)
    while(frontier != []):
        curr = heappop(frontier)
        if curr.toN in dir:
            continue
        if curr.dist > dists: continue
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

def maxFlow(case, dists):
    path = findPath(case.s, case.t, dists)
    
    while (path is not None):
        augment(path)
        path = findPath(case.s, case.t, dists)


cases = parse_start()
i = 1
for case in cases:
    #case.printCase()
    if i != 0:
        print("")
    print("Scenario "+str(i))
    for s in [5,10,20]:
        dists = (10*s)**2
        maxFlow(case, dists)
        print("In "+str(s)+" seconds "+str(case.t.flowOut())+" robot(s) can escape")
    i +=1