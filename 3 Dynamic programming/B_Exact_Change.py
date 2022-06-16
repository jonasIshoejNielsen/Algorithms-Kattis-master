from sys import stdin
import math
from functools import lru_cache

class Case(object):
    def __init__(self, amount):
        self.lst = []
        self.amount = amount
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortList(self):
        self.lst.sort(key=lambda e: e)


def parse_start():
    cases = []
    case = None
    coins = -1
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        if coins == -1:
            case = Case(int(split[0]))
            cases.append(case)
            ignore = True
        elif coins == -2: 
            coins = int(split[0])
            ignore = False      
        else:
            case.addToLst(int(split[0]))
        coins -= 1
    return cases
 
def printmatrix(matrix):
    [print(v) for v in matrix]
def printmatrixNoList(matrix):
    [print([e[0] for e in v]) for v in matrix]

def opt_nonrec(lst,n, W):
    OPT = [[(0,[]) for _ in range(W+1)] for _ in range(n+1)]     #OPT[n][w]  OPT[0][_]=0, OPT[_][0]=0
    for i in range(1, n+1):       #i=1,1,2,3,4,...,n-1
        for w in range(1,W+1):
            drop = OPT[i-1][w]
            currCoin = lst[i-1]
            take = (currCoin, [currCoin])
            if currCoin < w:
                optPre = OPT[i-1][w-currCoin]
                take = (take[0] + optPre[0], take[1] + optPre[1])
            if take[0] == drop[0]:
                OPT[i][w] = min([drop, take], key=lambda p: len(p[1]))
            elif take[0]>=w and drop[0]>=w:
                OPT[i][w] = min([drop, take], key=lambda p: p[0])
            else:
                OPT[i][w] = max([drop, take], key=lambda p: p[0])
    return OPT

    
cases = parse_start()
for case in cases:
    case.sortList()
    n = len(case.lst)
    OPT = opt_nonrec(case.lst, n, case.amount)
    print(f"{OPT[n][case.amount][0]} {len(OPT[n][case.amount][1])}")