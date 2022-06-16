from sys import stdin
from heapq import heappop, heappush

class Node(object):
    def __init__(self, value, negation):
        self.value = value
        self.negation = negation

    def __str__(self):
        if self.negation: return f"~{self.value}"
        else: return f"{self.value}"
    
    def printDetailed(self):
        print(self)
            
class Case(object):
    def __init__(self, numberOfNodes):
        self.clauses = []
        self.valuesToNodes = {}
    
    def addClause(self, split):
        clause = []
        for i in range(0, len(split), 2):
            curr = split[i]
            node = None
            key = None
            if curr[0] == "~":
                key = curr[1:]
                node = Node(key, True)
            else: 
                key = curr
                node = Node(key, False)
            if key in self.valuesToNodes:
                self.valuesToNodes[key].append(node)
            else:
                self.valuesToNodes[key] = [node]
            clause.append(node)
        self.clauses.append(clause)
    
    def finish(self):
        self.clauses = sorted(self.clauses, key = lambda lst: len(lst))
        
    def printCase(self):
        for lst in self.clauses:
            print(*lst, sep=' V ')
            for n in lst:
                n.printDetailed()    
            print("")
        


def parse_start():
    cases = []
    case = None
    nrOfClauses = 0
    for line_number, line in enumerate(stdin):
        if line_number == 0:
            continue
        split = line.rstrip('\r\n').split(" ")
        if nrOfClauses == 0:
            case = Case(int(split[0]))
            nrOfClauses =  int(split[1])
            cases.append(case)
            continue
        case.addClause(split)
        nrOfClauses -= 1
        
    return cases

def satisfiable(case, set, clauseIndex):
    result = None
    if clauseIndex >= len(case.clauses): return set
    clause = case.clauses[clauseIndex]
    
    for n in clause:
        if n.value in set:
            if n.negation != set[n.value]: 
                continue
            else:
                return satisfiable(case, set, clauseIndex+1)
    for n in clause:
        if n.value in set:
            continue
        oldValue = None
        if n.value in set:
            oldValue = set[n.value]
        set[n.value] = n.negation
        resn = satisfiable(case,set,clauseIndex+1)
        if resn is None:
            if oldValue is None:
                del set[n.value]
            else:
                set[n.value] = oldValue
            continue
        return resn 
    return result
        
    



cases = parse_start()
for case in cases:
    case.finish()
    res = satisfiable(case, {}, 0)
    if res is None: print("unsatisfiable")
    else: print("satisfiable")