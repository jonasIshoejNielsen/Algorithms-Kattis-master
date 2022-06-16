from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *
from queue import LifoQueue
#Single source shortest path, negative weights
#Bellan ford algorithm

class Node(object):
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
    
    def __str__(self):
        return str(self.value) + str(self.pos)
        
    def printSelf(self):
        print(self.value)

class Case(object):
    def __init__(self, numberOfNodes):
        self.nodes      = [None for i in range(numberOfNodes)]     #ignore nodes[0]
        self.s          = None
    
    def addLine(self, line, lineIndex):
        lst = [None for i in range(len(line))]
        for i in range(len(line)):
            lst[i] = Node(line[i], (lineIndex, i))
        self.nodes[lineIndex] = lst
    
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
 

def dijkstraFindNumberOfPaths(s, nodes):
    n = len(nodes)
    visited = [[0 for _ in range(n)] for _ in range(n)]
    frontier = []
    visited[0][0] = 1
    frontierNotTaken = []
    for row in range(n):
        for col in range(n):
            curr = nodes[row][col]
            if curr.value == "#":
                continue
            
            pathsToN = 0
            if row>0:
                pathsToN += visited[row-1][col]
            elif col == 0:
                continue        #row=0, col=0   //don't override s
            if col>0:
                pathsToN += visited[row][col-1]
            visited[row][col] = pathsToN
            if pathsToN == 0:
                continue
            for e in edgesAboveAndRight(row,col,n):
                frontierNotTaken.append(e)        # pick closets to end first
    return visited, frontierNotTaken

def edgesAboveAndRight(row,col,n):
    res = []
    if row>0: 
        res.append((row-1,col)) 
    if col>0: 
        res.append((row,col-1))
    return res

def edges(row,col,n):
    res = edgesAboveAndRight(row,col,n)
    if row<n-1: 
        res.append((row+1,col)) 
    if col<n-1: 
        res.append((row,col+1))
    return res

def bfs(nodes, visited, frontier):
    n = len(nodes)  
    while (frontier != []):
        e = frontier.pop()
        (row,col) = e
        if visited[row][col] > 0:
            continue
        if nodes[row][col].value == "#":
            continue
        if  row == n-1 and col == n-1:
            return True
        visited[row][col] = 1 
        for e in edges(row,col,n):
            frontierNotTaken.append(e)
    return False

def printPath(path):
    print("Path")
    for k in path:
        (t,e) = path[k]
        if e is None: print("   "+str(t)+" : None")
        else:         print("   "+str(t)+" : "+e.toString())



case = parse_start()
n = len(case.nodes)
#import time
#start_time = time.time()
dijk, frontierNotTaken = dijkstraFindNumberOfPaths(case.s, case.nodes)
#print("--- %s seconds ---" % (time.time() - start_time))
if dijk[n-1][n-1]>0:
    print(dijk[n-1][n-1] % ((2**31) -1))    
else:
    path = bfs(case.nodes, dijk, frontierNotTaken)
    if path:
        print("THE GAME IS A LIE")
    else:
        print("INCONCEIVABLE")
