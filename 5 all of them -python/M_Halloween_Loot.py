from sys import stdin
import math
from functools import lru_cache
import time

def getId(item):
    return item[0]
def getValueA(item):
    return item[1]
def getValueB(item):
    return item[2]

class Case(object):
    def __init__(self):
        self.lst = []
        self.capacityMax = 0
        self.capacityMin = 0
    
    def setList(self, lst):
        self.lst=lst
        for e in lst:
            a,b = getValueA(e), getValueB(e)
            if a>0:
                self.capacityMax += a
            else:
                self.capacityMin +=a
            if b>0:
                self.capacityMin -= b
            else:
                self.capacityMax -=b
        
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortList(self):
        #self.lst.sort(key=lambda e: getValueA(e) + getValueB(e))
        self.lst.reverse()


def parse_start():
    case    = Case()
    aList = None
    bList = None
    for (line_number, line) in enumerate(stdin):
        if line_number == 0:
            continue
        split = line.replace(" \n", "").split(" ")
        if line_number == 1:
            aList = [int(s) for s in split]
            continue
        if line_number == 2:
            bList = [int(s) for s in split]
            continue
    zippedList = [(i,a,b) for (i,(a,b)) in enumerate(list(zip(aList,bList)))] 
    case.setList(zippedList)
    return case
 
def printmatrix(matrix, Wmin, Wmax):
    [print([(i+Wmin,v) for (i,v) in enumerate(v)]) for v in matrix]


def inIndex(i, Wmin, Wmax):
    return i>=Wmin and i <= Wmax
def distFromZero(e):
    return abs(e)

def opt_nonrec(lst,n, Wmin, Wmax):
    OPT = [None for _ in range(n+1)]     #OPT[n][w]  OPT[0][_]=0, OPT[_][0]=0
    lastDict = [i for i in range(Wmin, Wmax+1)]
    OPT[0] = lastDict
    print(*lastDict)
    for i in range(1, n+1):       #i=1,1,2,3,4,...,n-1
        currItem = lst[i-1]
        a,b = getValueA(currItem), getValueB(currItem)
        newDict = [0 for i in range(Wmin, Wmax+1)]
        
        for w in range(Wmin, Wmax+1):
            
            if (not inIndex(w+a, Wmin, Wmax)):
                print(1, w, lastDict[w-b])
                newDict[w] = lastDict[w-b]
                continue
            if (not inIndex(w-b, Wmin, Wmax)):
                print(2, w, lastDict[w+a])
                newDict[w] = lastDict[w+a]
                continue

            drop = lastDict[w-b]
            take = lastDict[w+a]
            print(3, w, drop, take)
            newDict[w] = min(distFromZero(drop), distFromZero(take))

        OPT[i] = newDict
        lastDict = newDict
        break
    return OPT


def traverseBack(lst,OPT, n, Wmin, Wmax):
    print("")
    res = {}
    i = n
    w = 0
    while(i>0):
        currItem = lst[i-1]
        a,b = getValueA(currItem), getValueB(currItem)
        print("")
        print(i, a,b, currItem)
        if (not inIndex(w+a, Wmin, Wmax)):        #give to b
            print(i, w, a, "B",1)
            w -= b
            i -= 1
            res[getId(currItem)] = "B"
            continue
        if (not inIndex(w-b, Wmin, Wmax)):        #give to a
            print(i, w, b, "A",2)
            w += a
            i -= 1
            res[getId(currItem)] = "A"
            continue

        if OPT[i][w-Wmin] == OPT[i-1][w+a-Wmin]:
            print(i, w, b, "A",3)
            w += a
            res[getId(currItem)] = "A"
        else:
            print(i, w, a, "B",4)
            w -= b
            res[getId(currItem)] = "B"
        i -= 1
    return res  


case = parse_start()
#case.sortList()
n = len(case.lst)

OPT = opt_nonrec(case.lst, n, case.capacityMin, case.capacityMax)
print(*case.lst)
printmatrix(OPT, case.capacityMin, case.capacityMax)
res = traverseBack(case.lst, OPT, n, case.capacityMin, case.capacityMax)
resString = ""
for i in range(n):
    resString += res[i]

print(resString)
