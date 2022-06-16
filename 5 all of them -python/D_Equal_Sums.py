from sys import stdin
import math
from functools import lru_cache
import copy

class Case(object):
    def __init__(self, lst):
        self.lst = lst
        self.dict = {}
        self.lastDict = {}
    
    def sortList(self):
        self.lst.sort(key=lambda e: -e)
    
    def createDict(self):
        dict1 = {}
        for i in range(len(case.lst)):
            v = case.lst[i]
            dict1[v] = (i,{v})   
        self.dict = dict1 
        self.lastDict = dict1.copy()


def parse_start():
    cases = []
    case = None
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        case = Case([int(v) for v in split[1:]])
        cases.append(case)
    return cases

def equalSums(case):
    while len(case.lastDict) != 0:
        dictN = {}
        for i in range(len(case.lst)):
            v = case.lst[i]
            for key in case.lastDict:
                setMaxI,set = case.lastDict[key]
                if v <= setMaxI: continue       #no repeat
                if v in set: continue
                currSum = key+v
                newSet = set.copy()
                newSet.add(v)
                if currSum in case.dict:
                    fi,fset = case.dict[currSum]
                    if newSet == fset: continue
                    return (fset, newSet)
                dictN[currSum] = (max(i,setMaxI), newSet)
                case.dict[currSum] = (max(i,setMaxI),newSet)
        case.lastDict = dictN
    return None
    


cases = parse_start()
for i in range(len(cases)):
    print("Case #"+str(i+1)+":")
    case = cases[i]
    case.createDict()
    res = equalSums(case)
    if res is None: print("Impossible")
    else:
        set1,set2 = res
        print(*set1)
        print(*set2)
    