from sys import stdin

# Group K's implementation. (Beautiful)

class Organism(object):
    def __init__(self,name):
        self.name = name
        self.gene = ""

def read_penalties(filename):
    """
    Parses a file in the format of BLOSUM62.txt and creates a dictionary 
    mapping a pair of letters to their associated penalty
    filename: the location of the file to read
    """
    file = open(filename)
    
    penalties = {}
    letters = []
    for index,line in enumerate(file):
        if index < 6:
            continue
        split = line.rsplit()
        if index == 6:
            #Penalties is actually a dictionary of dictionaries! What!
            penalties = {x:{} for x in split}
            letters = split
            continue
        penalties[split[0]] = {x:int(v) for (x, v) in zip(letters, split[1:])}
    
    file.close()
    return penalties

def parse_input():
    """
    Parses organisms from standardin and creates a list of Organism objects each containing a name and their genetic sequence as a string
    """
    organisms = []
    current_organism = None
    for line in stdin:
        if line[0] == ">":
            split = line.rsplit()
            current_organism = Organism(split[0][1:])
            organisms.append(current_organism)
        else:
            current_organism.gene += line.replace("\n","")
    return organisms

def construct_table(o1, o2, penalties):
    """
    Using the naive iterative implementation (bottom up), constructs
    a table of m n elements containing optimal penalties for the match
    between two organisms
    o1: the first organism
    o2: the second organism
    penalties: a dictionary of penalties
    """
    m,n = len(o1.gene), len(o2.gene)
    M = [[0 for _ in range(n+1)] for _ in range(m+1) ]
    
    #Filling the first row and column with successively larger gap penalties
    for i in range(0, m):
        M[i+1][0] = M[i][0] + penalties["*"][o1.gene[i]]
    for j in range(0, n):
        M[0][j+1] = M[0][j] + penalties["*"][o2.gene[j]]

    #For each cell, choose the optimal penalty
    for i in range(m):
        for j in range(n):
            penalty = penalties[o1.gene[i]][o2.gene[j]]
            alignment = penalty + M[i][j]
            gap1 = penalties["*"][o1.gene[i]] + M[i][j+1]
            gap2 = penalties["*"][o2.gene[j]] + M[i+1][j]
            M[i+1][j+1] = max(alignment,gap1,gap2)

    return M

def trace_back(M, o1, o2, penalties):
    """
    Reconstructing the optimal alignment by tracing back through the table,
    selecting the previous cell that led to the current one.
    """
    i, j = len(o1.gene), len(o2.gene)
    results_o1, results_o2 = "", ""

    while i > 0 or j > 0:
        #If alignment was preferred over a gap
        if M[i][j] == M[i-1][j-1] + penalties[o1.gene[i-1]][o2.gene[j-1]] :
            i-=1
            j-=1
            results_o1 += o1.gene[i]
            results_o2 += o2.gene[j]
        #If a gap was introduced on the second gene
        elif M[i][j] == M[i-1][j] + penalties["*"][o1.gene[i-1]]:
            i -= 1
            results_o1 += o1.gene[i]
            results_o2 += "-"
        #If a gap was introduced on the first gene
        else:
            j-=1
            results_o1 += "-"
            results_o2 += o2.gene[j]

    # Reversing the strings since they are constructed in reverse order
    return results_o1[::-1], results_o2[::-1]

penalties = read_penalties("data/BLOSUM62.txt")
organisms = parse_input()

#Loop through every organism and match it with every other organism that hasn't 
#already matched with it
for i in range(len(organisms)):
    for j in range(i+1, len(organisms)):
        M = construct_table(organisms[i], organisms[j], penalties)
        res1,res2 = trace_back(M, organisms[i], organisms[j], penalties)
        print(organisms[i].name + "--" + organisms[j].name + ": "+ str(M[-1][-1]))
        print(res1)
        print(res2)
