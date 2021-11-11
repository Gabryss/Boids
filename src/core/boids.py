"""
Boids file
"""
from enums.colors import Color
from enums.config import Config
import random


def initialize_boids():
    pass




class Boid ():

    def __init__(self, position_p=random.uniform(0,100), velocity_p=random.uniform(0,Config.MAXSPEED.value), size_p=10.0, color_p=Color.RED.value):
        self.position = position_p
        self.velocity = velocity_p
        self.size = size_p
        self.color = color_p

    def __repr__(self):
        return "Boid: position={}, velocity={}, color={}".format(
            self.position, self.velocity, self.color)
    

    