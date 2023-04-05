import math

def euclaidean_distance(point, point1):
    x1, y1 = point
    x2, y2 = point1
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance
