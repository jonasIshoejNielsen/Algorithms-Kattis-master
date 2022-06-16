from sys import stdin
import math
from queue import PriorityQueue
from heapq import nlargest



class Case(object):
    def __init__(self, classrooms):
        self.lst = []
        self.classrooms = classrooms
    
    def addToList(self, items):
        self.lst.append(items)
    
    def sortLists(self):
        self.lst.sort(key=lambda e: e[0])


def parse_start():
    case = None
    for (line_number, line) in enumerate(stdin):
        split = line.replace(" \n", "").split(" ")
        if(line_number==0):
            case = Case(int(split[1]))
            continue
        case.addToList([int(v) for v in split])
    return case
 

def analyse(case):
    case.sortLists()
    roomsUsed = 0
    numbers = 0
    q = PriorityQueue()
    largest=None
    for v in case.lst:
        if(roomsUsed<case.classrooms):
            q.put((v[1], v[1]))
            if (largest is None or largest<v[1]):
                largest = v[1]
            roomsUsed +=1
            numbers += 1
            continue
        if(q.queue[0][1]<v[0]):
            if (largest is not None):
                if(largest<v[1]):
                    largest = v[1]
                if(q.queue[0][1]==largest):
                    largest = None
            q.get()
            q.put((v[1], v[1]))
            numbers += 1
            continue   
        if(largest is None):
            largest = nlargest(1, q.queue, key=lambda e:e[1])[0][0]
        if (largest > v[1]):
            q2 = PriorityQueue()
            q2.put((v[1], v[1]))
            addedLargest = False
            newLargest = v[1]
            for oldElement in q.queue:
                if(not addedLargest and oldElement[0]==largest):
                    addedLargest=True
                    continue
                if newLargest < oldElement[0]:
                    newLargest = oldElement[0]
                q2.put(oldElement)
            q=q2
            largest = newLargest
            
    print(numbers)

        
        
case = parse_start()
analyse(case)