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
    def __init__(self, numberOfNodes):
        self.t          = Node("t")
        self.s          = Node("s")
        self.nodes      = [Node(i) for i in range(numberOfNodes+1)]     #ignore nodes[0]

    def addEdgeToT(self, index, value):
        node = self.nodes[index]
        node.addEdgeTo(self.t, -value)

    def addEdgeToS(self, index, value):
        node = self.nodes[index]
        self.s.addEdgeTo(node, value)
        
    def addEdgesFromTo(self, index, lst):
        node = self.nodes[index]
        for i in lst:
            self.nodes[i].addEdgeTo(node, float('inf'))
            
        
    def printCase(self):
        self.s.printSelf()
        self.t.printSelf()
        for n in self.nodes:
            n.printSelf()

def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.rstrip('\r\n').split(" ")
        if(line_number==0):
            case = Case(int(split[0]))
            continue
        value = int(split[0]) -int(split[1])
        if value<0:
            case.addEdgeToT(line_number,value)
        if value>0:
            case.addEdgeToS(line_number, value)
        case.addEdgesFromTo(line_number, [int(i) for i in split[3:]])
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
print(case.s.flowOut())