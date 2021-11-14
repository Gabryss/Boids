import math


def magnitude(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def dot(a, b):
    return sum(i * j for i, j in zip(a, b))


def angle_between(a, b):
    angle = math.degrees(math.acos(dot(a, b) / (magnitude(*a) * magnitude(*b))))
    return angle