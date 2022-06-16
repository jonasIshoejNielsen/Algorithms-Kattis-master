from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

class Edge(object):
    def __init__(self, fromN, toN, cost, value):
        self.fromN  = fromN
        self.toN    = toN
        self.cost   = cost
        self.value  = value
        
      
    def __lt__(self, other):
        return self.value < other.value
        
    def toString (self):
        return str(self.fromN.value) + "  -"+str(self.cost)+"-  "+str(self.toN.value)
        
    
class Node(object):
    def __init__(self, value, pos):
        self.edges = []
        self.edgesRev = []
        self.value = value
        self.pos = pos
    
    def addEdgeTo(self, node, cost, leftDown,edgeValue):    
        edge = Edge(self, node, cost, edgeValue)
        if leftDown:
            self.edges.append(edge)
        else:
            self.edgesRev.append(edge)
        return edge

    def __str__(self):
        return str(self.value) + str(self.pos)
        
    def printSelf(self):
        print(self.value)
        print(len(self.edges), len(self.edgesRev))
        for e in self.edges:
            print("    " + e.toString())
        for e in self.edgesRev:
            print("    " + e.toString())

class Case(object):
    def __init__(self, numberOfNodes):
        self.nodes      = [[None for i in range(numberOfNodes)] for i in range(numberOfNodes)]     #ignore nodes[0]
        self.s          = None
    
    def addLine(self, line, lineIndex):
        for i in range(len(line)):
            self.nodes[lineIndex][i] = Node(line[i], (lineIndex, i))
        for i in range(0,len(self.nodes)):
            if self.nodes[lineIndex][i].value == "#":
                continue
            edgeValue =  (lineIndex,i)
            if i>0 and self.nodes[lineIndex][i-1].value == ".":
                self.nodes[lineIndex][i-1].addEdgeTo(self.nodes[lineIndex][i], 1, True, edgeValue)
                self.nodes[lineIndex][i].addEdgeTo(self.nodes[lineIndex][i-1], 1, False,edgeValue)
            if lineIndex > 0 and self.nodes[lineIndex-1][i].value == ".":
                self.nodes[lineIndex-1][i].addEdgeTo(self.nodes[lineIndex][i], 1, True,edgeValue)
                self.nodes[lineIndex][i].addEdgeTo(self.nodes[lineIndex-1][i], 1, False,edgeValue)
    
    def finish(self):
        n = len(self.nodes[0])
        self.s = self.nodes[0][0]
        self.t = self.nodes[n-1][n-1]
    
    def printCase(self):
        self.s.printSelf()
        for l in self.nodes:
            print(*[n.value for n in l])     
        
                

def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.rstrip('\r\n').split(" ")
        if line_number == 0:
            case = Case(int(split[0]))
            continue
        split = list(split[0])
        case.addLine(split, line_number-1)
    case.finish()
    return case

def RemoveIfThere(set, item):
    if item in set:
        set.discard(item)
 

def dijkstraFindNumberOfPaths(s):
    visited = {}
    frontier = []
    visited[s] = 1
    
    for e in s.edges:
        heappush(frontier, (e.value, e))
    while(frontier != []):
        _,currEdge = heappop(frontier)
        if currEdge.toN in visited:
            continue
        
        pathsToN = 0
        for e in currEdge.toN.edgesRev:
            if e.toN not in visited:
                continue
            pathsToN += visited[e.toN]
        
        visited[currEdge.toN] = pathsToN
        for e in currEdge.toN.edges:
            heappush(frontier, (e.value, e))
    return visited   

def bfs(s, t):
    visited = {}
    frontier = []
    visited[s] = None
    for e in s.edges:
        frontier.append(e)
    for e in s.edgesRev:
        frontier.append(e)
    
    while(frontier != []):
        currEdge = frontier.pop()
        visited[currEdge.toN] = currEdge.fromN 
        for e in currEdge.toN.edges:
            if e.toN not in visited:
                frontier.append(e)
        for e in currEdge.toN.edgesRev:
            if e.toN not in visited:
                frontier.append(e)
        if currEdge.toN == t:
            return True
    
    return False

def printPath(path):
    print("Path")
    for k in path:
        (t,e) = path[k]
        if e is None: print("   "+str(t)+" : None")
        else:         print("   "+str(t)+" : "+e.toString())



case = parse_start()
n = len(case.nodes)
dijk = dijkstraFindNumberOfPaths(case.s)

if case.t in dijk:
    print(dijk[case.t] % ((2**31) -1))
else:
    path = bfs(case.s, case.t)
    if path:
        print("THE GAME IS A LIE")
    else:
        print("INCONCEIVABLE")