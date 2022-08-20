import math


def magnitude(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def dot(a, b):
    return sum(i * j for i, j in zip(a, b))


def angle_between(a, b):
    magnitude_angle = magnitude(*a) * magnitude(*b)
    if magnitude_angle != 0.0 :
        angle = math.degrees(math.acos(dot(a, b) / magnitude_angle))
        return angle
    else:
        return 0.0
    

def normalize(a):
    mag = magnitude(*a)
    if mag != 0:
        return [i / mag for i in a]
    else:
        return a