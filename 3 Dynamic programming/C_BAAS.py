from sys import stdin
import math
from functools import lru_cache
import copy

class Case(object):
    def __init__(self, costs):
        self.lst = [[]]
        self.leaves = [True]
        self.costs = [0]
        for v in costs:
            self.costs.append(int(v))
        self.costs.append(0)        #last one who is depepndent on all the leaves
        self.newIndex = 0
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, items):
        self.lst.append([int(v) for v in items[1:]])
        self.leaves.append(True)
        for v in items[1:]:
            self.leaves[int(v)] = False
    
    def sortList(self):
        self.lst.sort(key=lambda e: e)


def parse_start():
    case = None
    readTimes = False
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        if (not readTimes):
            case = Case(split)
            readTimes = True
            continue
        case.addToLst(split)
    return case
 
def printmatrix(matrix):
    [print(v) for v in matrix]
def printmatrixNoList(matrix):
    [print([e[0] for e in v]) for v in matrix]
    
def all_same(items):
    return all(x[1] == items[0][1] for x in items)

def opt_nonrec(lst, costs, n):
    OPTMax = [0 for _ in range(n)]

    for i in range(1, n):
        currentCost = costs[i]      
        if len(lst[i]) == 0:
            OPTMax[i] = currentCost
            continue  
        OPTMax[i] = max([OPTMax[v] for v in  lst[i]]) + currentCost
        
    results = [OPTMax[n-1]-costs[1]]
    for i in range(2,n):
        OPTCurr = copy.copy(OPTMax)
        OPTCurr[i] = OPTMax[i]-costs[i]
        for y in range(i+1,n):
            changedDeppendencies = False
            for v in lst[y]:
                if OPTMax[v] != OPTCurr[v]:
                    changedDeppendencies = True
                    break
            if changedDeppendencies:
                OPTCurr[y] = max([OPTCurr[v] for v in  lst[y]]) + costs[y]
        results.append(OPTCurr[n-1])
    return results

    
case = parse_start()

leaves = []
for i in range(len(case.leaves)):
    if(case.leaves[i]):
        leaves.append(i)
case.addToLst(leaves)

n = len(case.lst)
results = opt_nonrec(case.lst, case.costs, n)
print(min(results))