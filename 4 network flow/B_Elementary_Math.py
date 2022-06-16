from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

class Edge(object):
    def __init__(self, fromN, toN, capacity, value):
        self.fromN = fromN
        self.toN = toN
        self.capacity = capacity
        self.value = value
        
    def toString (self):
        return str(self.fromN.value) + "  -"+str(self.capacity)+"-  "+str(self.toN.value)+"    "+self.value
    
    def decreaseCapacityBy(self, b):
        self.capacity -=b
        reverseEdge = self.toN.findEdgeTo(self.fromN, self.value)
        if reverseEdge is not None:
            reverseEdge.capacity += b
        else:
            self.toN.edges.append(Edge(self.toN, self.fromN, b, self.value))
        if self.capacity<=0:
            self.fromN.edges.remove(self)
        
    def __lt__(self, other):
        return -self.capacity < -other.capacity
    
class Node(object):
    def __init__(self, value):
        self.edges = []
        self.value = value
    
    def setEdgesTo(self, nodes, capacity, value):
        self.edges = [Edge(self, node, capacity, value) for node in nodes]
    def addEdgeTo(self, node, capacity, value):
        self.edges.append(Edge(self, node, capacity, value))
    def findEdgeTo(self, node, value):
        for e in self.edges:
            if e.toN == node and e.value == value:
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

class Case(object):
    def __init__(self):
        self.t          = Node("t")
        self.s          = Node("s")
        self.pairs      = []
        self.results    = {}

    def addPair(self, int1, int2):
        node = Node((int1, int2))
        self.pairs.append(node)
        self.s.addEdgeTo(node, 1, "")
        results = [(int1+int2, "+"), (int1*int2, "*"), (int1-int2, "-")]
        for r in results:
            if not (r[0] in self.results):
                resNode = Node(str(r[0]))
                self.results[r[0]] = resNode 
                resNode.addEdgeTo(self.t,1,"")   
            node.addEdgeTo(self.results[r[0]], 1, r[1])

    
    def printCase(self):
        self.s.printSelf()
        self.t.printSelf()
        for e in self.pairs:
            e.printSelf()
        for key in self.results:
            self.results[key].printSelf()

def parse_start():
    case = Case()
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        case.addPair(int(split[0]), int(split[1]) )
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

if len(case.s.edges) !=0:
    print("impossible")
else:
    for pairN in case.pairs:
        lst = ["+", "-", "*"]
        for e in pairN.edges:
            if e.toN.value == "s":
                continue
            lst.remove(e.value)
        if lst[0] == "+":
            print(str(pairN.value[0])+" + "+str(pairN.value[1]) +" = "+str(pairN.value[0]+pairN.value[1]))
        elif lst[0] == "*":
            print(str(pairN.value[0])+" * "+str(pairN.value[1]) +" = "+str(pairN.value[0]*pairN.value[1]))
        elif lst[0] == "-":
            print(str(pairN.value[0])+" - "+str(pairN.value[1]) +" = "+str(pairN.value[0]-pairN.value[1]))
  