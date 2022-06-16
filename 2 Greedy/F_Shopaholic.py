from sys import stdin
import math



class Case(object):
    def __init__(self, items):
        self.lst = items
    
    def sortLists(self):
        self.lst.sort(reverse = True)


def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        split = line.replace(" \n", "").split(" ")
        case = Case([int(v) for v in split])
    return case
 

def analyse(case):
    case.sortLists()
    saved = 0
    i = 0
    for v in case.lst:
        i+=1
        if(i<3):
            continue
        saved +=v
        i=0
        
        
    print(saved)
        
        
case = parse_start()
analyse(case)