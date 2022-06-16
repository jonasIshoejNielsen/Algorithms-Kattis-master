from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *
#Single source shortest path, time table
class Edge(object):
    def __init__(self, fromN, toN):
        self.fromN  = fromN
        self.toN    = toN
        self.cost = 0
        
      
    def __lt__(self, other):
        return self.cost < other.cost
        
    def toString (self):
        return str(self.fromN.id) + "  --  "+str(self.toN.id)
        
    
class Node(object):
    def __init__(self, id, has, requires):
        self.edges = []
        self.id = id
        self.has = has
        self.requires = requires
    
    def addEdgeTo(self, node):
        self.edges.append(Edge(self, node))
    
       
    def printSelf(self):
        print(self.id)
        for e in self.edges:
            print("    " + e.toString())

class Case(object):
    def __init__(self, n, zeroRequires):
        self.s          = Node(0, 0, zeroRequires)
        self.nodes      = [None for _ in range(n+1)]
        self.nodes[0]   = self.s
    
    def addNode(self, i, prev, have, require):
        self.nodes[i] = Node(i, have, require)
        self.nodes[prev].addEdgeTo(self.nodes[i])
   
            
    def printCase(self):
        print("S:")
        self.s.printSelf()
        for n in self.nodes:
            n.printSelf()

def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        split = [int(v) for v in line.rstrip('\r\n').split(" ")]
        if line_number == 0:
            case = Case(split[0], split[1])
            continue
        case.addNode(line_number, split[0], split[2], split[1])
    
    return case

def findBest(case):
    best = case.s.requires
    frontier = [(best, case.s)]
    while(frontier != []):
        (prevRequires,node) = frontier.pop()
        neededToPass = node.requires - node.has
        valueForNode = max(neededToPass, prevRequires-node.has)
        best = min(best,valueForNode)
        
        for e in node.edges:
            frontier.append((valueForNode, e.toN))
    return best
    


case = parse_start()
best = findBest(case)
print(best)