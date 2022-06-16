from sys import stdin
import math
from queue import PriorityQueue


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
        split = line.replace(" \n", "").split(" ")
        if(line_number==0):
            continue
        case.addToLst((int(split[0]), int(split[1])))   #time needed sea-level
    return case
 

def analyse(case):
    case.sortLists()
    stores = 0
    waterLevel=0
    timesTaken = PriorityQueue()
    for v in case.lst:
        if(waterLevel + v[0] <= v[1]):
            waterLevel += v[0]
            stores +=1
            timesTaken.put((v[0], v[0] ))
            continue
        lst = []
        while(not timesTaken.empty()):
            curr = timesTaken.get()[0]
            if(v[0]<curr):
                lst.append(v[0])
                waterLevel += v[0] - curr
                break
            lst.append(curr)
        for x in lst:
            timesTaken.put((x, x))    
    print(stores)
        
        
case = parse_start()
analyse(case)