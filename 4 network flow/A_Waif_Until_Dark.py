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
        return self.fromN.description + "  -"+str(self.capacity)+"-  "+self.toN.description
    
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
    
class Node(object):
    def __init__(self, description):
        self.edges = []
        self.description = description
    def setEdgesTo(self, nodes, capacity):
        self.edges = [Edge(self, node, capacity) for node in nodes]
    def findEdgeTo(self, node):
        for e in self.edges:
            if e.toN == node:
                return e
        return None
    def flowOut(self):
        sum = 0
        for e in self.edges:
            sum += e.capacity
        return sum
    def printSelf(self):
        print(self.description)
        for e in self.edges:
            print("    " + e.toString())

class Case(object):
    def __init__(self,numberOfChildren, numberOfToys, numberOfCategories):
        self.t          = Node("t")
        self.s          = Node("s")
        self.children   = [Node("child"+str(i+1)) for i in range(numberOfChildren)]
        self.toys       = [Node("toy"+str(i+1)) for i in range(numberOfToys)]
        for toy in self.toys:
            toy.setEdgesTo([self.t], 1)
        self.categories = [Node("cat"+str(i+1)) for i in range(numberOfCategories)]

        self.s.setEdgesTo(self.children, 1)
        self.maxFlow = self.s.flowOut()

    def addChild(self, childNr, toys):
        self.children[childNr-1].setEdgesTo([self.toys[t-1] for t in toys], 1)
        
    def addCategory(self, category, toys, capacity):
        cat = self.categories[category-1]
        for toy in toys:
            self.toys[toy-1].setEdgesTo([cat], 1)
        cat.setEdgesTo([self.t], capacity)
    def printCase(self):
        self.s.printSelf()
        self.t.printSelf()
        for c in self.children:
            c.printSelf()
        for t in self.toys:
            t.printSelf()
        for c in self.categories:
            c.printSelf()


def parse_start():
    case = None
    readChildren   = None
    category       = 1
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if(line_number==0):
            case = Case(int(split[0]), int(split[1]), int(split[2]))
            readChildren = int(split[0])
            continue
        if (readChildren>0):
            case.addChild(line_number, [int(v) for v in split[1:]])
            readChildren -= 1
            continue
        
        #readCategories
        case.addCategory(category, [int(v) for v in split[1:-1]], int(split[-1]) )
        
        category+=1
    return case
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
        path = findPath(case.s, case.t)

case = parse_start()
maxFlow(case)
print(case.maxFlow-case.s.flowOut())