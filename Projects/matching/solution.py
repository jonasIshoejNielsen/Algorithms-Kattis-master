from sys import stdin

class Person(object):
    def __init__(self, line):
        id, name = line.split(" ")
        self.id = int(id) - 1
        self.name = name.rsplit()[0]
        self.prefs = None
        self.partner = None
        self.is_proposer = self.id % 2 == 0

    def set_prefs(self, prefs):
        prefs =  [int(pref) - 1 for pref in prefs]
        if self.is_proposer:
            self.prefs = prefs
        else:
            self.prefs = {id: n-rank for (rank, id) in enumerate(prefs)}

persons = []
free_m = []
n = 0

def parse_preferences(start_index):
    for (_, line) in enumerate(stdin, start_index):
        split = line.replace(" \n", "").split(" ")
        id = int(split[0][:-1]) - 1
        prefs = split[1:]
        person = persons[id]
        person.set_prefs(prefs)

def parse_names(start_index):
    for (line_number, line) in enumerate(stdin, start_index):
        if line == "\n":
            parse_preferences(line_number)
            break
        else:
            person = Person(line)
            persons.append(person)
            if person.is_proposer: free_m.append(person.id)
def parse_start():     
    for (line_number, line) in enumerate(stdin):
        if line[0] == "#":
            pass
        elif line[0] == "n":
            n = int(line[2:])
            parse_names(line_number)
        else: break

def run_Gale_Shapley():
    while len(free_m) > 0 and len(persons[free_m[0]].prefs) > 0:
        m = persons[free_m[0]]
        w = persons[m.prefs.pop(0)]

        if w.partner is None:
            w.partner = m
            m.partner = w
            free_m.pop(0)
        elif w.prefs[m.id] > w.prefs[w.partner.id]:
            free_m.pop(0)
            free_m.append(w.partner.id)
            w.partner = m
            m.partner = w

def print_result():
    for p in persons:
        if p.id % 2 == 0:
            print(p.name + " -- " + p.partner.name)

parse_start()
run_Gale_Shapley()
print_result()
