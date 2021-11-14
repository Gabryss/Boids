"""
Boids file
"""
from enums.config import Config
import random
import pyglet

def initialize_boids(nb=20):
    boids_list=[]
    for i in range(20):
        boids_list.append(Boid())
    return boids_list




class Boid ():

    def __init__(self, position_p=random.uniform(0,100), velocity_p=random.uniform(0,Config.MAXSPEED.value), size_p=3, color_p=Config.DEFAULT_COLOR_RED.value):
        self.position = position_p
        self.velocity = velocity_p
        self.size = size_p
        self.color = color_p

        #Triangle shape parameters : p1(x), p1(y), p2(x), p2(y), p3(x), p3(y)
        self.shape = pyglet.shapes.Triangle(self.position+(2*self.size),self.position, self.position-self.size, self.position+self.size, self.position-self.size, self.position-self.size, self.color, batch=Config.BATCH.value)

    def __repr__(self):
        return "Boid: position={}, velocity={}, color={}".format(
            self.position, self.velocity, self.color)
    
    def get_size(self):
        return self.size
    
    def get_color(self):
        return self.color
    
    def get_velocity(self):
        return self.velocity
    
    def get_position(self):
        return self.position
    
    def set_size(self,size_p):
        self.size = size_p
    
    def set_color(self, color_p):
        self.color = color_p
    
    def set_velocity(self, velocity_p):
        self.velocity = velocity_p
    
    def set_position(self, position_p):
        self.position = position_p
    