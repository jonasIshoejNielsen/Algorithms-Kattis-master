from sys import stdin
import math

class Case(object):
    def __init__(self):
        self.lst = []
    def addToList(self, lst):
        self.lst.append(lst)
    def sortLists(self):
        self.lst.sort()

cases=[]
def parse_start():
    case = None
    custommers = 0
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        if case is None:
            case = Case()
            cases.append(case)
            custommers=int(split[0])
            if(custommers<=0):
                case = None
        else:
            case.addToList(sum([int(v) for v in (split[1:])]))
            custommers -=1
            if(custommers<=0):
                case = None
            

def analyse():
    for case in cases:
        case.sortLists()
        totalWait = 0
        waited=0
        for v in case.lst:
            waited += v
            totalWait += waited
            
        print(format(totalWait/len(case.lst), '.10f'))
        
        
parse_start()
analyse()
