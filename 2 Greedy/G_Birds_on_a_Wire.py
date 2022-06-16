from sys import stdin
import math



class Case(object):
    def __init__(self, l, d):
        self.l = l
        self.d=d
        self.lst = []
    def addToLst(self, item):
        self.lst.append(item)
    
    def sortLists(self):
        self.lst.sort()


def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if(line_number==0):
            case = Case(int(split[0]), int(split[1]))
            continue
        case.addToLst(int(split[0]))
    return case
 

def analyse(case):
    case.sortLists()
    birds = 0
    i = 0
    v=6
    while(True):
        if(v>case.l-6): break
        if(i>=len(case.lst)):
            birds+=1
            v+=case.d
            continue
        bird = case.lst[i]
        if(abs(bird-v)<case.d):
            v = bird + case.d
            i+=1
            continue
        
        birds+=1
        v+=case.d

        
    print(birds)
        
        
case = parse_start()
analyse(case)