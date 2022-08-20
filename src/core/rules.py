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
    steering = np.array([0.0, 0.0])
    if len(nearby_boids)> 0:
        avg_vec = np.array([0.0, 0.0])

        for boid in nearby_boids:
            avg_vec += boid.velocity

            # sum_x += boid.velocity[0]
            # sum_y += boid.velocity[1]

        # if (sum_x,sum_y) != (0.0,0.0):
        avg_vec /= len(nearby_boids)
        avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * Config.MAXSPEED.value
        steering = avg_vec - me.velocity
        return steering
    else:
        return steering


def cohesion(me, nearby_boids):
    
    steering = np.array([0.0, 0.0])
    if len(nearby_boids) > 0:
        center_of_mass = np.array([0.0, 0.0])

        for boid in nearby_boids:
            center_of_mass += boid.position

        center_of_mass /=  len(nearby_boids)
        vect_to_compare = center_of_mass - me.position
        # if np.linalg.norm(vect_to_compare) > 0:
        #     vect_to_compare = (vect_to_compare / np.linalg.norm(vect_to_compare)) * Config.MAXSPEED.value
        # steering = vect_to_compare - me.velocity
        steering = vect_to_compare

        
        # if np.linalg.norm(steering) > Config.MAXSPEED.value:
        #     steering = (steering / np.linalg.norm(steering)) * Config.MAXSPEED.value
    return steering
            #average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            #return [ average_x - me.position[0], average_y - me.position[1] ]



def separation(me, nearby_boids):
    # nearby_objs = (
    #         obj for obj in objs
    #         if (obj != me and
    #             utils.magnitude(obj.position[0] - me.position[0],
    #                              obj.position[1] - me.position[1])
    #             - me.size <= Config.DEFAULT_COHESION_DIST.value))

    # c = [0.0, 0.0]
    # for obj in nearby_objs:
    #     diff = obj.position[0] - me.position[0], obj.position[1] - me.position[1]
    #     inv_sqr_magnitude = 1 / ((utils.magnitude(*diff) - me.size) ** 2)

    #     c[0] = c[0] - inv_sqr_magnitude * diff[0]
    #     c[1] = c[1] - inv_sqr_magnitude * diff[1]
    # return c

    steering = np.zeros(2)
    total = 0
    avg_vector = np.zeros(2)
    if type(me.position) is tuple:
        me.position = np.array(me.position)
    for boid in nearby_boids:
        distance = np.linalg.norm(boid.position - me.position)
        # if me.position != boid.position:
        if (me.position-boid.position).any() != 0:
        
            diff = me.position - boid.position
            diff /= distance
            avg_vector += diff
            total += 1
    if total > 0:
        avg_vector /= total
        avg_vector = avg_vector
        if np.linalg.norm(steering) > 0:
            avg_vector = (avg_vector / np.linalg.norm(steering)) * me.Config.MAXSPEED.value
        steering = avg_vector - me.velocity
        if np.linalg.norm(steering)> Config.DEFAULT_ALIGNMENT_FORCE.value:
            steering = (steering /np.linalg.norm(steering)) * Config.DEFAULT_ALIGNMENT_FORCE.value

    return steering
