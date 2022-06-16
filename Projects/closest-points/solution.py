from sys import stdin
from math import sqrt

class Point(object):
    def __init__(self,line):
        self.id = line[0]
        self.x = float(line[1])
        self.y = float(line[2])

    def distance(self,p):
        return sqrt((self.x-p.x)**2+(self.y-p.y)**2)

    def __str__(self):
        return f"{self.id}: {self.x} , {self.y}"

def parse():
    points = []
    parsing_points = False
    for linenumber,line in enumerate(stdin):
        split = line.rsplit()
        if len(split) == 0:
            pass
        elif split[0] == "NODE_COORD_SECTION":
            parsing_points = True
        elif not parsing_points:
            pass
        elif split[0] == "EOF":
            break
        else:
            points.append(Point(split))
    return points

def closest_point(lst):
    if len(lst) > 2:
        l = len(lst)//2
        l_point = lst[l]
        left, right = lst[0:l] , lst[l:]

        min_distance_left = closest_point(left)
        min_distance_right = closest_point(right)

        min_distance = min(min_distance_left , min_distance_right)
        
        mid_list = filter(lambda p: abs(p.x-l_point.x) < min_distance , lst)

        mid_list = sorted(mid_list,key=lambda p:p.y)

        for i in range(len(mid_list)):
            for j in range(1,min(16,len(mid_list[i:]))):
                v = mid_list[i].distance(mid_list[i+j])
                min_distance = min(min_distance,v)
        
        return min_distance

    elif len(lst) == 2:
        return lst[0].distance(lst[1])
    else:
        return float("inf")
        
points = parse()
sorted_points = sorted(points,key=lambda p: p.x)
distance = closest_point(sorted_points)
print(f"{len(sorted_points)} {distance}")