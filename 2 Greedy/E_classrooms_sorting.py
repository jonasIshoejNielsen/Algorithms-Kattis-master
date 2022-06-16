from sys import stdin
import math



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
 
def insertionSort(lst): 
    for i in range(1, len(lst)): 
        key = lst[i] 
        j = i-1
        while j >=0 and key < lst[j] : 
                lst[j+1] = lst[j] 
                j -= 1
        lst[j+1] = key 

def insertionSortRev(lst): 
    for i in range(len(lst)-2, -1, -1): 
        key = lst[i] 
        j = i+1
        while j <len(lst) and key > lst[j] : 
                lst[j-1] = lst[j] 
                j += 1
        lst[j-1] = key 
        
def analyse(case):
    case.sortLists()
    roomsUsed = 0
    numbers = 0
    q = []
    for v in case.lst:
        if(roomsUsed<case.classrooms):
            q.append(v[1])
            roomsUsed +=1
            numbers += 1
            if(roomsUsed>=case.classrooms):
                insertionSort(q)
            continue
        if(q[0]<v[0]):
            q[0]=v[1]
            q.sort()
            numbers += 1
            continue   
        if (q[len(q)-1] > v[1]):
            q[len(q)-1] = v[1]
            insertionSortRev(q)

        
        
    print(numbers)
        
        
case = parse_start()
analyse(case)