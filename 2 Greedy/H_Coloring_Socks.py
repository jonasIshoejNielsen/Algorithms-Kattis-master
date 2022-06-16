from sys import stdin
import math



class Case(object):
    def __init__(self, c, k):
        self.c = c
        self.k = k
        self.lst = []
    
    def setList(self, lst):
        self.lst=lst
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortLists(self):
        self.lst.sort()


def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if(line_number==0):
            case = Case(int(split[1]), int(split[2]))
            continue
        case.setList([int(v) for v in split])
    return case
 

def analyse(case):
    case.sortLists()
    groups = 0
    currGroupSize = 0
    currGroupMaxValue=0
    for sock in case.lst:
        if(currGroupSize>=case.c):
            currGroupSize=0
        if(currGroupSize==0 or sock > currGroupMaxValue):
            currGroupSize = 1
            groups+=1
            currGroupMaxValue = sock + case.k
            continue
        currGroupSize +=1
            

        
    print(groups)
        
        
case = parse_start()
analyse(case)