from sys import stdin
import math
from functools import lru_cache
import time

def getId(item):
    return item[0]
def getValue(item):
    return item[1]
def getWeight(item):
    return item[2]

class Case(object):
    def __init__(self, capacity):
        self.lst = []
        self.capacity = capacity
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortList(self):
        self.lst.sort(key=lambda e: getWeight(e))


def parse_start():
    cases   = []
    case    = None
    items   = 0
    itemID  = 0
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if items == 0:
            case = Case(int(split[0]))
            cases.append(case)
            items = int(split[1])
            itemID = 0
            continue
        case.addToLst((itemID, int(split[0]), int(split[1])))
        items -= 1
        itemID +=1
    return cases
 
def printmatrix(matrix):
    [print(v) for v in matrix]
def printmatrixNoList(matrix):
    [print([e[0] for e in v]) for v in matrix]


def opt_nonrec_old(lst,n, W):
    OPT = [[0 for _ in range(W+1)] for _ in range(n+1)]     #OPT[n][w]  OPT[0][_]=0, OPT[_][0]=0
    for i in range(1, n+1):       #i=1,1,2,3,4,...,n-1
        currItem = lst[i-1]
        currWeight = getWeight(currItem)
        for w in range(1,W+1):
            drop = OPT[i-1][w]
            if currWeight > w:
                OPT[i][w] = drop
                continue
            take = getValue(currItem) + OPT[i-1][w-currWeight]
            OPT[i][w] = max(drop, take)
    return OPT


def opt_nonrec(lst,n, W):
    OPT = [None for _ in range(n+1)]     #OPT[n][w]  OPT[0][_]=0, OPT[_][0]=0
    lastDict = [0 for _ in range(W+1)]
    OPT[0] = lastDict
    for i in range(1, n+1):       #i=1,1,2,3,4,...,n-1
        currItem = lst[i-1]
        currWeight = getWeight(currItem)
        newDict = lastDict.copy()
        for w in range(currWeight,W+1):
            drop = lastDict[w]
            take = getValue(currItem) + lastDict[w-currWeight]
            newDict[w] = max(drop, take)
        
        OPT[i] = newDict
        lastDict = newDict
    return OPT


def traverseBack(lst,OPT, n, W):
    res = []
    i = n
    w = W
    while(i>0 and w>0):
        if OPT[i][w] == OPT[i-1][w]:
            i -= 1
            continue
        i -= 1
        currItem = lst[i]
        w   -= getWeight(currItem)
        res.append(getId(currItem))
    return res  

cases = parse_start()
for case in cases:
    case.sortList()
    n = len(case.lst)
    
    OPT = opt_nonrec(case.lst, n, case.capacity)

    res = traverseBack(case.lst, OPT, n, case.capacity)
    print(len(res))
    print(*res)
