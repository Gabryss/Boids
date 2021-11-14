"""
Boids file
"""
import math
from enums.config import Config
import random
import pyglet
import boot
import numpy as np

def initialize_boid(width, height):
    return(Boid(position_p=[random.uniform(0,width), random.uniform(0,height)], velocity_p=[random.uniform(-20,20), random.uniform(-20,20)]))


class Boid():

    def __init__(self, position_p=[random.uniform(0,500),random.uniform(0,500)], velocity_p=[random.uniform(-20,20), random.uniform(-20,20)], size_p=3, color_p=Config.DEFAULT_COLOR_RED.value):
        self.position = position_p
        self.velocity = velocity_p
        self.size = size_p
        self.color = color_p
        self.time = 0
        self.batch = Config.BATCH.value

        #Boid shape parameters : center_point [x1,y1], lower_wing [x2,y2], noze [x3,y3], upper_wing[x4,y4], color, batch
        self.shape = pyglet.shapes.Polygon([self.position[0],self.position[1]],[self.position[0]-self.size,self.position[1]-self.size],[self.position[0]+2*self.size,self.position[1]],[self.position[0]-self.size,self.position[1]+self.size],color=self.color, batch=Config.BATCH.value)


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
    
    def nearby_boids(self,boids):
        pass
    
    def _rotate_shape(self):
        """Rotate base image using the velocity and assign to image."""
        angle = -np.rad2deg(np.angle(self.velocity[0] + 1j * self.velocity[1]))
        self.shape.rotation = angle

    
    def update(self, delta_time):
        self.time += delta_time

        self.shape.x += self.velocity[0] * delta_time
        self.shape.y += self.velocity[1] * delta_time

        self.shape.x1 += self.velocity[0] * delta_time
        self.shape.y1 += self.velocity[1] * delta_time

        self.shape.x2 += self.velocity[0] * delta_time
        self.shape.y2 += self.velocity[1] * delta_time

        self.shape.x3 += self.velocity[0] * delta_time
        self.shape.y3 += self.velocity[1] * delta_time

        self._rotate_shape()

        if self.shape.x > boot.window.width:
            self.shape.x = 0

            self.shape.x1 = -self.size

            self.shape.x2 = 2*self.size

            self.shape.x3 = -self.size
        
        if self.shape.x < 0:
            self.shape.x = boot.window.width

            self.shape.x1 = boot.window.width - self.size

            self.shape.x2 = boot.window.width + 2*self.size

            self.shape.x3 = boot.window.width - self.size

        if self.shape.y > boot.window.height:
            self.shape.y = 0

            self.shape.y1 = -self.size

            self.shape.y2 = 0

            self.shape.y3 = +self.size
        
        if self.shape.y < 0:
            self.shape.y = boot.window.height

            self.shape.y1 = boot.window.height - self.size

            self.shape.y2 = boot.window.height

            self.shape.y3 = boot.window.height + self.size
    