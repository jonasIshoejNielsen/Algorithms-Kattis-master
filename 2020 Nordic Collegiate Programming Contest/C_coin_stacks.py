from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

class Case(object):
    def __init__(self, lst):
        self.lst = []
        for i in range(len(lst)):
            item = int(lst[i])
            if item<=0:
                continue
            heappush(self.lst, (-item, (i+1, item)))

    def sortList(self):
        self.lst.sort(key=lambda e: -e[1])


def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        case = Case(split)
    return case
 
    
case = parse_start()
#case.sortList()
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
    
