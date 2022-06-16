from sys import stdin
import math
from functools import lru_cache

class Case(object):
    def __init__(self):
        self.lst = []
        self.W = 1000
        self.largest = self.W
        self.done = False
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, item):
        self.lst.append(item)
        self.largest = min(self.largest, item)
        if item == 1000:
            self.done=True
    
    def sortList(self):
        self.lst.sort(key=lambda e: e)


def parse_start():
    case = Case()
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        case.addToLst(int(line))
    return case
 
def printmatrix(matrix):
    [print(v) for v in matrix]
def printmatrixNoList(matrix):
    [print([e[0] for e in v]) for v in matrix]

def opt_nonrec(lst,n, W, largest):
    OPT = [[False for _ in range(W+largest+1)] for _ in range(n+1)]
    OPT[0][0] =True
    bestWeight = 0
    newMax = W+largest+1
    done = False
    for i in range(1, n+1):
        if done:
            break
        vi = lst[i-1]
        for w in range(0,newMax):
            drop = OPT[i-1][w]
            if w-vi < 0:
                take = False
            else: 
                take = OPT[i-1][w-vi]
            best = drop or take
            if best:
                OPT[i][w] = True
                if abs(bestWeight-W) == abs(w-W):
                    bestWeight = max(bestWeight,w)
                    if bestWeight>W:
                        newMax = bestWeight
                    elif bestWeight == W:
                        done = True
                        break
                elif abs(bestWeight-W) > abs(w-W):
                    bestWeight = w
                    if bestWeight>W:
                        newMax = bestWeight
                    elif bestWeight == W:
                        done = True
                        break
    print(bestWeight)  
    return (bestWeight,OPT)

if __name__ == "__main__":
    case = parse_start()
    if case.done:
        print(1000)
    else:
        #case.sortList()
        n = len(case.lst)
        (bestWeight,OPT) = opt_nonrec(case.lst, n, case.W, case.largest)
        #printmatrix(OPT)
        #print(f"{OPT[n][case.W-1]}")