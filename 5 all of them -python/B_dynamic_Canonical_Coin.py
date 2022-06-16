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
        self.lst.sort(key=lambda e: -e)


def parse_start():
    case = Case()
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        case.setList([int(v) for v in split])
    return case
 
def opt_nonrec(lst, n, maxCoin):
    OPT = [0 for _ in range(maxCoin*2 + 1)]
    
    done = False
    for i in range(1,maxCoin*2 + 1):
        index = 0
        while(lst[index]>i):
            index += 1
        take = 1 + OPT[i-lst[index]]
        for v in range(index+1, n):
            if 1 + OPT[i-lst[v]] < take:
                print("non-canonical")
                done = True
                break
        if done:
            break
        OPT[i] = take
    if not done:
        print("canonical")

    
case = parse_start()
case.sortList()

n = len(case.lst)
maxCoin = case.lst[0]
opt_nonrec(case.lst, n, maxCoin)