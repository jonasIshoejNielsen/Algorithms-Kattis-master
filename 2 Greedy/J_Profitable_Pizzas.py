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
        self.lst.sort(key=lambda e: e[0])


def parse_start():
    case = Case()
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if(line_number==0):
            continue
        case.addToLst((int(split[0]), int(split[1])))   #deadline reward
    return case
 

def analyse(case):
    case.sortLists()
    moneyEarned = 0
    timeSpent=0
    rewardsEarned = PriorityQueue()
    print(case.lst)
    for v in case.lst:
        if(timeSpent + 1 <= v[0]):
            moneyEarned += v[1]
            timeSpent +=1
            rewardsEarned.put((v[1], v[1] ))
            continue
        lowestRewardEarned = rewardsEarned.queue[0][1]
        if(v[1]>lowestRewardEarned):
            moneyEarned += v[1] - lowestRewardEarned
            rewardsEarned.get()
            rewardsEarned.put((v[1], v[1] ))
    print(rewardsEarned.queue)
    print(moneyEarned)
    
case = parse_start()
analyse(case)