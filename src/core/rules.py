"""
Rules for the boids

## Alignment

## Cohesion

## Separation

## Collision avoidance
"""
import utils
from enums.config import Config
import numpy as np
# from math import Vector

def alignment(me, nearby_boids):
    if len(nearby_boids)> 0:
        # print("Yamete")
        sum_x, sum_y = 0.0, 0.0
        for boid in nearby_boids:
                sum_x += boid.velocity[0]
                sum_y += boid.velocity[1]
        
        if (sum_x,sum_y) != (0,0):
            average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [average_x - me.velocity[0], average_y - me.velocity[1]]
    else:
        return [0.0,0.0]


def cohesion(me, nearby_boids):
    if len(nearby_boids) > 0:
        sum_x, sum_y = 0.0, 0.0
        for boid in nearby_boids:
            sum_x += boid.position[0]
            sum_y += boid.position[1]
        if (sum_x,sum_y) != (0,0):
            average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [ average_x - me.position[0], average_y - me.position[1] ]
    else:
        return [0.0, 0.0]


def separation():
    pass


def collision_avoidance(me, objs):
    nearby_objs = (
            obj for obj in objs
            if (obj != me and
                utils.magnitude(obj.position[0] - me.position[0],
                                 obj.position[1] - me.position[1])
                - me.size <= Config.DEFAULT_COHESION_DIST.value))

    c = [0.0, 0.0]
    for obj in nearby_objs:
        diff = obj.position[0] - me.position[0], obj.position[1] - me.position[1]
        inv_sqr_magnitude = 1 / ((utils.magnitude(*diff) - me.size) ** 2)

        c[0] = c[0] - inv_sqr_magnitude * diff[0]
        c[1] = c[1] - inv_sqr_magnitude * diff[1]
    return c