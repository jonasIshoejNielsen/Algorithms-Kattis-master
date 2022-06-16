from sys import stdin
import math
from functools import lru_cache
import copy

class Case(object):
    def __init__(self):
        self.lst = []
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortList(self):
        self.lst.sort(key=lambda e: (e[0], e[1]))


def parse_start():
    case = None
    cases = []
    for (line_number, line) in enumerate(stdin):
        if line_number == 0:
            continue
        if(line_number%2==1):
            case = Case()
            cases.append(case)
            continue
        split = line.replace(" \n", "").split(" ")
        w = None
        for v in split:
            if w is None:
                w=int(v)
                continue
            item = (w, int(v))
            case.addToLst(item)
            w = None
    return cases
 
def opt_nonrec(lst, n):
    currentClass = 0
    visited = [None for v in range(n)]
    for i in range(0,n):
        if visited[i] is not None:
            continue
        largestH = lst[i][1]
        currentVisited = visited[i]
        lastAdded = None
        for j in range(i,n):
            if visited[j] is not None:
                continue
            if largestH > lst[j][1]:   #can't fit
                continue
            if currentVisited is None:
                currentClass += 1
                currentVisited = (currentClass, None, None)
                visited[i] = (currentVisited[0], currentVisited[1], j)
                visited[j] = (currentVisited[0], i, None)
            else:
                visited[lastAdded] = (currentVisited[0], visited[lastAdded][1], j)
                visited[j] = (currentVisited[0], lastAdded, None)
            lastAdded=j
            largestH = max(largestH, lst[j][1])
            currentVisited = visited[i]
    print(currentClass)

    
cases = parse_start()
for case in cases:
    case.sortList()

    n = len(case.lst)
    opt_nonrec(case.lst, n)