from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

def getT(f):
    return f[0]
def getMin(f):
    return f[1]
def getMax(f):
    return f[2]

class Case(object):
    def __init__(self):
        self.faucets = []
        self.recipes = []
        
    def addFaucets(self, split):
        self.faucets.append(split)
    
    def addRecepe(self, split):
        self.recipes.append((split[0]*split[1], split[1]))
    
    def sortList(self):
        self.faucets.sort(key=lambda e: -getT(e))


def parse_start():
    case = Case()
    faucets = 0
    for (line_number, line) in enumerate(stdin):
        split = [int(v) for v in line.replace(" \n", "").split(" ")]
        if(line_number==0):
            faucets = split[0]
            continue
        if(faucets>0):
            case.addFaucets(split)
        elif faucets < 0:
            case.addRecepe(split)
        faucets -= 1
    return case

cache = {}
def findBest(case, recepe, i, currSumX, currXT):
    curr = case.faucets[i]
    toReachMax = recepe[1] - currSumX
    if (i,currSumX, currXT) in cache:
        return cache[(i,currSumX, currXT)]
    
    if i == len(case.faucets)-1:
        if getMin(curr) > toReachMax:
            return -1               # reduce currSumX given
        if getMax(curr) < toReachMax:
            return 1                # increase currSumX given
        finalXTSum = (currXT + toReachMax*getT(curr))
        if finalXTSum == recepe[0]:
            return 0
        elif finalXTSum > recepe[0]:
            return -1
        else:
            return 1
    
    currMin = getMin(curr)
    currMax = min(toReachMax, getMax(curr))
    if currMax < currMin:
        return -1
    while(True):
        x = math.ceil((currMax + currMin) / 2)
        newSumX = currSumX + x
        newSumXT = currXT + x*getT(curr)
        res = findBest(case,recepe, i+1, newSumX, currXT + x*getT(curr))
        
        cache[(i+1,newSumX, newSumXT)] = res
        
        if res == 0:
            return 0
        if(currMin == currMax):
            return res
        if res <0:
            currMax =x-1
        else:
            currMin = x+1
    

    
case = parse_start()
case.sortList()
for i in range(len(case.recipes)):
    cache = {}
    res = findBest(case, case.recipes[i], 0, 0, 0)
    if res == 0:
        print("yes")
    else:
        print("no")

"""
res = []
failed = False
while(case.lst != []):
    (_,(i1,v1)) = heappop(case.lst)
    if case.lst == []:
        failed = True
        print("no")
        break
    (_,(i2,v2)) = heappop(case.lst)
    if(v1-1 > 0):
        heappush(case.lst,(-(v1-1), (i1,v1-1)))
    if(v2-1 > 0):
        heappush(case.lst,(-(v2-1), (i2,v2-1)))
    res.append(str(i1)+ " " + str(i2))
    
if not failed:
    print("yes")
    for r in res:
        print(r)
    
"""