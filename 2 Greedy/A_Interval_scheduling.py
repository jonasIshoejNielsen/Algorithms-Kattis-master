from sys import stdin

n=0  
jobs=[]
def parse_start():
    for (line_number, line) in enumerate(stdin):
        if line_number==0:
            n= int(line)
        else:
            split = line.replace(" \n", "").split(" ")
            jobs.append((int(split[0]),  int(split[1])))

def analyse():
    jobs.sort(key=lambda e: e[1])
    schedules = 0
    lastStarted = None
    for j in jobs:
        if lastStarted is None:
            lastStarted = j
            schedules=schedules+1
        elif j[0] >= lastStarted[1]:
            lastStarted = j
            schedules=schedules+1
    print(schedules)
            

parse_start()
analyse()
