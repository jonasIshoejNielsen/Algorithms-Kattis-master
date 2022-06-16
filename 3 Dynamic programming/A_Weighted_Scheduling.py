from sys import stdin
import math
from functools import lru_cache

class Case(object):
    def __init__(self):
        self.lst = []
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortLists(self):
        self.lst.sort(key=lambda e: e[1])


def parse_start():
    case = Case()
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        
        case.addToLst((int(split[0]), int(split[1]), int(split[2])))   #deadline reward
    return case
 
 

def binarySearch(data, val):
    lo, hi = 0, len(data) - 1
    best_ind = lo
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if data[mid] < val:
            lo = mid + 1
        elif data[mid] > val:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind] 
        if abs(data[mid] - val) < abs(data[best_ind] - val):
            best_ind = mid
    return best_ind
 
def binarySearch(lst, j):
    val = lst[j][0]
    lo, hi = 0, j-1
    while lo <= hi:
        mid = (hi + lo) // 2
        if lst[mid][1] <= val:
            if lst[mid+1][1] <= val:
                lo = mid + 1
            else:
                return mid
        else :
            hi = mid - 1

    return -1

@lru_cache(maxsize=10**5)
def p(j):
    return binarySearch(lst, j)

def opt_nonrec(lst):
    n= len(lst)
    OPT = [-1]*(n)          #-1,-1,-1,...,-1
    OPT[0] = lst[0][2]
    for i in range(1, n):   #i=1,1,2,3,4,...,n-1
        drop = OPT[i-1]
        prev = p(i)
        take = lst[i][2]
        if prev != -1:
            take = take + OPT[prev]
        res = max(drop, take)
        OPT[i] = res
    print( OPT[n-1])
    
case = parse_start()
case.sortLists()
lst = case.lst
opt_nonrec(case.lst)
