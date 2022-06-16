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

def closest_point(lstx, lsty):
    if len(lstx) > 2:
        l = len(lstx)//2
        l_point = lstx[l]
        leftx, rightx = lstx[0:l] , lstx[l:]
        lefty, righty = list(filter(lambda p: (p.x<l_point.x) , lsty)) , list(filter(lambda p: (p.x>l_point.x) , lsty))
        
        
        min_distance_left, points_left     = closest_point(leftx, lefty)
        min_distance_right, points_right   = closest_point(rightx, righty)
        
        min_distance = 0
        best_points = []
        if min_distance_left < min_distance_right:
            min_distance, best_points = min_distance_left, points_left
        else:
            min_distance, best_points = min_distance_right, points_right
       
        mid_list = list(filter(lambda p: abs(p.x-l_point.x) < min_distance , lsty))
        
        for i in range(len(mid_list)):
            for j in range(1,min(16,len(mid_list[i:]))):
                v = mid_list[i].distance(mid_list[i+j])
                if v<min_distance:
                    min_distance = v
                    best_points = [mid_list[i], mid_list[i+j]]
        
        return min_distance, best_points

    elif len(lstx) == 2:
        return lstx[0].distance(lstx[1]), lstx
    else:
        return float("inf"), []
        
points = parse()
sorted_pointsX = sorted(points,key=lambda p: p.x)
sorted_pointsY = sorted(points,key=lambda p: p.y)
distance, points = closest_point(sorted_pointsX, sorted_pointsY)
print(f"{len(points)} {distance}")
print(f"{len(points)} {distance} {points[0].id} {points[1].id}")