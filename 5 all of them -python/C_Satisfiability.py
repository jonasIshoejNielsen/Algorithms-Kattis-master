from sys import stdin
from heapq import heappop, heappush

class Edge(object):
    def __init__(self, fromN, toN):
        self.toN        = toN
        self.fromN      = fromN
        self.reverse    = None

    def __str__(self):
        return f"     {self.fromN}  --  {self.toN}"

class Node(object):
    def __init__(self, value, negation):
        self.value = value
        self.edges = []
        self.negation = negation
        
    def add_edge(self, e):
        self.edges.append(e)
        
    def findEdgeTo(self, node):
        for e in self.edges:
            if e.toN == node:
                return e
        return None
    
    def __str__(self):
        if self.negation: return f"~{self.value}"
        else: return f"{self.value}"
    
    def printDetailed(self):
        print(self)
        for e in self.edges:
            print(e)
            
class Case(object):
    def __init__(self, numberOfNodes):
        self.clauses = []
        self.valuesToNodes = {}
        
    def createEdges(self, u, v):
        existingEdge = u.findEdgeTo(v)
        if existingEdge is None:
            e1 = Edge(u,v)
            e2 = Edge(v,u)
            e1.reverse, e2.reverse = e2, e1
            u.add_edge(e1)
            v.add_edge(e2)
    
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
        for key in self.valuesToNodes:
            lst = self.valuesToNodes[key]
            for i in range(0, len(lst), 1):
                for j in range(i+1, len(lst), 1):
                    if lst[i].negation == lst[j].negation: continue
                    self.createEdges(lst[i], lst[j])
        for clause in self.clauses:
            for i in range(0, len(clause), 1):
                for j in range(i+1, len(clause), 1):
                    self.createEdges(clause[i], clause[j])
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

