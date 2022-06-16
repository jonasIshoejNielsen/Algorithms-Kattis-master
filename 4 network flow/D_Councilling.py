from sys import stdin
import math
from functools import lru_cache
import copy
from heapq import *

class Edge(object):
    def __init__(self, fromN, toN, capacity):
        self.fromN = fromN
        self.toN = toN
        self.capacity = capacity
        
    def toString (self):
        return str(self.fromN.name) + "  -"+str(self.capacity)+"-  "+str(self.toN.name)
    
    def decreaseCapacityBy(self, b):
        self.capacity -=b
        reverseEdge = self.toN.findEdgeTo(self.fromN)
        if reverseEdge is not None:
            reverseEdge.capacity += b
        else:
            self.toN.edges.append(Edge(self.toN, self.fromN, b))
        if self.capacity<=0:
            self.fromN.edges.remove(self)
        
    def __lt__(self, other):
        return -self.capacity < -other.capacity

class Node(object):
    def __init__(self, name):
        self.edges = []
        self.name = name
    
    def setEdgesTo(self, nodes, capacity):
        self.edges = [Edge(self, node, capacity) for node in nodes]
    def addEdgeTo(self, node, capacity):
        self.edges.append(Edge(self, node, capacity))
    def findEdgeTo(self, node):
        for e in self.edges:
            if e.toN == node:
                return e
        return None
        
    def flowOut(self):
        sum = 0
        for e in self.edges:
            sum += e.capacity
        return sum
    def printSelf(self):
        print(self.name)
        for e in self.edges:
            print("    " + e.toString())

class Case(object):
    def __init__(self):
        self.t          = Node("t")
        self.s          = Node("s")
        self.members    = []
        self.party      = {}
        self.clubs   = {}

    def addMember(self, member, party, clubs):
        
        if not (party in self.party):
            self.party[party] = Node(party)

        memberNode = Node(member)
        self.members.append(memberNode)
        partyNode = self.party[party]
        partyNode.addEdgeTo(memberNode, 1)
        
        
        for c in clubs:
            if not (c in self.clubs):
                clubNode = Node(c)
                self.clubs[c] = clubNode 
                clubNode.addEdgeTo(self.t,1) 
            clubNode = self.clubs[c]
            memberNode.addEdgeTo(clubNode, 1)
    
    def finish(self):
        numberOfCouncilMembers = len(self.clubs)
        numberAloowed = ((numberOfCouncilMembers + (numberOfCouncilMembers % 2)) / 2) -1        #e.g. n=1-->0, n=2-->0, n=3-->1, n=4-->1, n=5-->2, n=6-->2
        for key in self.party:
            self.s.addEdgeTo(self.party[key], numberAloowed)
    
    def printCase(self):
        self.s.printSelf()
        self.t.printSelf()
        for e in self.members:
            e.printSelf()
        for key in self.party:
            self.party[key].printSelf()
        for key in self.clubs:
            self.clubs[key].printSelf()
    
def parse_start():
    cases = []
    case = None
    membersLeft = 0
    for (line_number, line) in enumerate(stdin):
        if(line_number==0):
            continue
        if membersLeft == 0:
            membersLeft=int(line)
            case = Case()
            cases.append(case)
            continue    
        split = line.rstrip('\r\n').split(" ")
        case.addMember(split[0],split[1], split[3:] )
        membersLeft -= 1
    return cases


def printPath(lst):
    print("Path:")
    for e in lst:
        print("    " + e.toString())

def findPath(s,t):
    dir = {}
    frontier = []
    for e in s.edges:
        heappush(frontier, e)
    while(frontier != []):
        curr = heappop(frontier)
        if curr.toN in dir:
            continue
        dir[curr.toN] = curr
        for e in curr.toN.edges:
            heappush(frontier, e)
        if t in dir:
            lst = []
            curr = t
            while(curr != s):
                lst.append(dir[curr])
                curr = dir[curr].fromN
            lst.reverse()
            return lst
    return None
def findBottleNeck(lst):
    bottleneck = None
    for e in lst:
        if bottleneck is None:
            bottleneck = e.capacity
        else:
            bottleneck = min(bottleneck, e.capacity)
    return bottleneck

def augment(path):
    bottleneck = findBottleNeck(path)
    for e in path:
        e.decreaseCapacityBy(bottleneck)

def maxFlow(case):
    path = findPath(case.s, case.t)
    while (path is not None):
        augment(path)
        path = findPath(case.s, case.t)


cases = parse_start()
first = True
for case in cases:
    case.finish()
    maxFlow(case)
    if first:
       first = False 
    else:
        print("")
    if len(case.t.edges) != len(case.clubs):
        print("Impossible.")
    else:
        for clubKey in case.clubs:
            club = case.clubs[clubKey]
            if len(club.edges) != 1:
                print("error")
                print(club.printSelf())
                raise Exception("invalid number of edges")
            member = club.edges[0].toN
            print(member.name + " "+club.name) 
 rss feed for new problems |