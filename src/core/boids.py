"""
Boids file
"""
from pyglet.shapes import Polygon,_ShapeBase
from enums.config import Config
import random
import pyglet
import boot
import numpy as np
import rules
import utils

def initialize_boid(width, height):
    return(Boid(position_p=[random.uniform(0,width), random.uniform(0,height)], velocity_p=[random.uniform(-20,20), random.uniform(-20,20)]))


class Boid():

    def __init__(self, position_p=[random.uniform(0,500),random.uniform(0,500)], velocity_p=[random.uniform(-20,20), random.uniform(-20,20)], size_p=3, color_p=Config.DEFAULT_COLOR_GREEN.value):
        self.position = position_p
        self.velocity = velocity_p
        self.size = size_p
        self.color = color_p
        self.time = 0
        self.bounds = [[self.position[0],self.position[1]],[self.position[0]-self.size,self.position[1]-self.size],[self.position[0]+2*self.size,self.position[1]],[self.position[0]-self.size,self.position[1]+self.size]]
        self.batch = Config.BATCH.value
        self.all_boids = []

        #Boid shape parameters : center_point [x1,y1], lower_wing [x2,y2], noze [x3,y3], upper_wing[x4,y4], color, batch
        self.shape = pyglet.shapes.Polygon(self.bounds[0],self.bounds[1],self.bounds[2],self.bounds[3],color=self.color, batch=Config.BATCH.value)


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
    
    def get_all_boids(self, all_boids_p):
        self.all_boids = all_boids_p
    
    def nearby_boids(self,boids):
        for boid in boids:
            diff = (boid.position[0] - self.position[0], boid.position[1] - self.position[1])
            if (boid != self and
                    utils.magnitude(*diff) <= Config.DEFAULT_ALIGNMENT_DIST.value and
                    utils.angle_between(self.velocity, diff) <= Config.VISIBLE_ANGLE.value):
                yield boid
        return
    
    @property
    def x1(self):
        """X coordinate of the shape.

        :type: int or float
        """
        return self._coordinates[1][0]

    @x1.setter
    def x1(self, value):
        self._coordinates[1][0] = value
        self._update_position()
    
    @property
    def x2(self):
        """X coordinate of the shape.

        :type: int or float
        """
        return self._coordinates[2][0]
    
    @x2.setter
    def x2(self, value):
        self._coordinates[2][0] = value
        self._update_position()
    
    @property
    def x3(self):
        """X coordinate of the shape.

        :type: int or float
        """
        return self._coordinates[3][0]
    
    @x3.setter
    def x3(self, value):
        self._coordinates[3][0] = value
        self._update_position()
    
    @property
    def y1(self):
        """Y coordinate of the shape.

        :type: int or float
        """
        return self._coordinates[1][1]

    @y1.setter
    def y1(self, value):
        self._coordinates[1][1] = value
        self._update_position()
    
    @property
    def y2(self):
        """Y coordinate of the shape.

        :type: int or float
        """
        return self._coordinates[2][1]
    
    @y2.setter
    def y2(self, value):
        self._coordinates[2][1] = value
        self._update_position()
    
    @property
    def y3(self):
        """Y coordinate of the shape.

        :type: int or float
        """
        return self._coordinates[3][1]

    @y3.setter
    def y3(self, value):
        self._coordinates[3][1] = value
        self._update_position()

    
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
        
        #Edge limit of the window
        #If a boid touch a border, he will reapear at the opposite one
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
        
        nearby_boids = self.all_boids
        # print(len(nearby_boids))

        alignment_vector = rules.alignment(self, nearby_boids)
        cohesion_vector = rules.cohesion(self, nearby_boids)
        separation_vector = rules.collision_avoidance(self, nearby_boids)

        self.forces = [ #(Config.DEFAULT_ALIGNMENT_FORCE.value, alignment_vector),
                        (Config.DEFAULT_COHESION_FORCE.value, cohesion_vector),
                        (Config.DEFAULT_SEPARATION_FORCE.value, separation_vector)] 

        # print(self.velocity[0], "Old x velocity")
        # print(self.velocity[1], "Old y velocity")

        for force, vector in self.forces:
            # print("Force : ", force, " vector : ", vector)
            self.velocity[0] += force * vector[0]
            self.velocity[1] += force * vector[1]


        # print(self.velocity[0], "New x velocity")
        # print(self.velocity[1], "New y velocity")




        # ensure that the boid's velocity is <= _MAX_SPEED
        # self.velocity = vector.limit_magnitude(self.velocity, _MAX_SPEED, _MIN_SPEED)
    