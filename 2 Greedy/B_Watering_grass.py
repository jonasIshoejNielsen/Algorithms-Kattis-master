from sys import stdin
import math

class Case(object):
    def __init__(self, n, l, w):
        self.n = int(n)
        self.l = int(l)
        self.w = int(w)
        self.sprinklers = []

    def addCase(self, case):
        self.sprinklers.append(case)
    def getSprinklers(self):
        return self.sprinklers
    def sortSprinklers(self):
        self.sprinklers.sort(key=lambda e: e[0]-e[1])

cases=[]
def parse_start():
    case = None
    halfW = 0
    wSquare = 0
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if len(split) == 3:
            case = Case(split[0], split[1], split[2])
            cases.append(case)
            halfW = case.w/2
            wSquare = halfW**2
        else:
            if (halfW > int(split[1])):
                continue
            r  = math.sqrt((int(split[1])**2)- wSquare)
            case.addCase((int(split[0]), r) )

def analyse():
    for case in cases:
        case.sortSprinklers()  
        used = 0
        lastUsed = None
        cover = 0
        lastCovered = 0
        for j in case.getSprinklers() :
            if(cover >= case.l):
                break
            if lastUsed is None:
                if(j[0]-j[1] >0  ):
                    continue
                lastUsed = j
                cover = j[0]+j[1]
                used=1
            elif (cover > (j[0]+ j[1])):
                continue
            elif (cover < (j[0]- j[1])):
                continue
            else:
                lastUsed = j
                if(lastCovered>=j[0]- j[1]):
                    cover = j[0]+j[1]
                    continue
                lastCovered = cover
                cover = j[0]+j[1]
                used=used+1
        if(cover < case.l):
            print(-1)
        else:
            print(used)
        
            

parse_start()
analyse()
