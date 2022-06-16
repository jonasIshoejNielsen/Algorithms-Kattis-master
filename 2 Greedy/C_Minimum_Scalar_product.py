from sys import stdin
import math

class Case(object):
    def __init__(self):
        self.lst1 = []
        self.lst1 = []
    def sortLists(self):
        self.lst1.sort()
        self.lst2.sort(reverse = True)

cases=[]
def parse_start():
    case = None
    addFirst=True
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        if case is None:
            case = Case()
            cases.append(case)
            addFirst=True
        elif(addFirst):
            addFirst=False
            case.lst1 = [int(v) for v in split]
        else:
            case.lst2 = [int(v) for v in split]
            case = None
            

def analyse():
    caseNr=0
    for case in cases:
        case.sortLists()
        sum = 0
        caseNr += 1
        for i in range(len(case.lst1)) :
            #print(case.lst1[i], case.lst2[i])
            sum += case.lst1[i]*case.lst2[i]
        print("Case #"+str(caseNr)+": "+str(sum))
        
        
parse_start()
analyse()
