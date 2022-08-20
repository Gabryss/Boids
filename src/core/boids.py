"""
Boids core file
"""
from distutils.command.config import config
from pyglet.shapes import Polygon,_ShapeBase
from enums.config import Config
import random
import pyglet
import numpy as np
import rules
import utils

def initialize_boid(width, height):
    return(Boid(position_p=[random.uniform(0,width), random.uniform(0,height)], velocity_p=[random.uniform(-20,20), random.uniform(-20,20)]))


class Boid():

    def __init__(self, position_p=np.array([random.uniform(0,500),random.uniform(0,500)]), velocity_p=np.array([random.uniform(-20,20), random.uniform(-20,20)]), size_p=3, color_p=Config.DEFAULT_COLOR_GREEN.value):
        self.position = position_p
        self.velocity = velocity_p
        self.size = size_p
        self.color = color_p
        self.acceleration = np.array([0.0,0.0])
        self.time = 0
        self.bounds = [[self.position[0],self.position[1]],[self.position[0]-self.size,self.position[1]-self.size],[self.position[0]+2*self.size,self.position[1]],[self.position[0]-self.size,self.position[1]+self.size]]
        self.batch = Config.BATCH.value
        self.nearby_boids = []

        # self.image = pyglet.image.load("/home/ggarcia/Documents/Boids/src/core/boid2.png")
        # self.image.anchor_x = self.image.width // 2
        # self.image.anchor_y = self.image.height // 2
        # self.image.blit(self.position[0], self.position[1])
        #Boid shape parameters : center_point [x1,y1], lower_wing [x2,y2], noze [x3,y3], upper_wing[x4,y4], color, batch
        self.shape = pyglet.shapes.Polygon(self.bounds[0],self.bounds[1],self.bounds[2],self.bounds[3],color=self.color, batch=Config.BATCH.value)


    
    
    def discover_nearby_boids(self,boids):
        """
        Discover nearby boids.
        """
        nearby_boids = []
        for boid in boids:
            # print(type(boid.get_position()), type(self.position))
            # diff = boid.get_position() - self.position
            diff = [other_boid - this_boid for other_boid, this_boid in zip(boid.get_position(), self.position)]
            # diff = (boid.position[0] - self.position[0], boid.position[1] - self.position[1])

            # print(diff,"diff")
            if (boid != self and
                    utils.magnitude(*diff) <= Config.DEFAULT_ALIGNMENT_DIST.value and
                    utils.angle_between(self.velocity, diff) <= Config.VISIBLE_ANGLE.value):
                nearby_boids.append(boid)
        self.nearby_boids = nearby_boids
        return nearby_boids

        # nearby_boids = []
        # for boid in boids:
        #     diff = [other_boid - this_boid for other_boid, this_boid in zip(boid.get_position(), self.position)]
        #     if np.linalg.norm(diff) <= Config.MAXDIST.value:
        #         nearby_boids.append(boid)
        # self.nearby_boids = nearby_boids
        # return nearby_boids

    
    def _rotate_shape(self):
        """
        Rotate base image using the velocity and assign to image.
        """
        angle = -np.rad2deg(np.angle(self.velocity[0] + 1j * self.velocity[1]))
        self.shape.rotation = angle


    def _edge(self):
        """
        Check if the boid is outside the window and if so, reflect it.
        If the boid touch a border of the window, it will respawn in the opposite border.
        """       

        if self.shape.x > Config.WINDOW_WIDTH.value:
            self.shape.x = 0

            self.shape.x1 = -self.size

            self.shape.x2 = 2*self.size

            self.shape.x3 = -self.size

            self.position = (0, self.shape.y)
        
        if self.shape.x < 0:
            self.shape.x = Config.WINDOW_WIDTH.value

            self.shape.x1 = Config.WINDOW_WIDTH.value - self.size

            self.shape.x2 = Config.WINDOW_WIDTH.value + 2*self.size

            self.shape.x3 = Config.WINDOW_WIDTH.value - self.size

            self.position = (Config.WINDOW_WIDTH.value, self.shape.y)

        if self.shape.y > Config.WINDOW_HEIGHT.value:
            self.shape.y = 0

            self.shape.y1 = -self.size

            self.shape.y2 = 0

            self.shape.y3 = +self.size

            self.position = (self.shape.x, 0)

        
        if self.shape.y < 0:
            self.shape.y = Config.WINDOW_HEIGHT.value

            self.shape.y1 = Config.WINDOW_HEIGHT.value - self.size

            self.shape.y2 = Config.WINDOW_HEIGHT.value

            self.shape.y3 = Config.WINDOW_HEIGHT.value + self.size

            self.position = (self.shape.x, Config.WINDOW_HEIGHT.value)
    

    def _apply_forces(self, boids):
        """
        Apply the forces to the boid.
        """
        alignment_vector = rules.alignment(self,boids)
        cohesion_vector = rules.cohesion(self,boids)
        separation_vector = rules.separation(self,boids)
        self.forces = [ 
                        # (Config.DEFAULT_ALIGNMENT_FORCE.value, alignment_vector),
                        (Config.DEFAULT_COHESION_FORCE.value, cohesion_vector),
                        (Config.DEFAULT_SEPARATION_FORCE.value, separation_vector),
                        ]
        
        for force, vector in self.forces:
            if force and vector is not None:
                self.acceleration += vector * force

        self.velocity += self.acceleration
        

    def _limit_velocity(self):
        """
        Limit the velocity to the maximum velocity.
        """
        if np.linalg.norm(self.velocity) > Config.MAXSPEED.value:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * Config.MAXSPEED.value


    def _update_position(self, delta_time_p):
        """
        Update the boid's position and velocity.
        """
        self.time += delta_time_p
        
        self.shape.x += self.velocity[0] * delta_time_p
        self.shape.y += self.velocity[1] * delta_time_p

        self.shape.x1 += self.velocity[0] * delta_time_p
        self.shape.y1 += self.velocity[1] * delta_time_p
        
        self.shape.x2 += self.velocity[0] * delta_time_p
        self.shape.y2 += self.velocity[1] * delta_time_p

        self.shape.x3 += self.velocity[0] * delta_time_p
        self.shape.y3 += self.velocity[1] * delta_time_p
        

    def update(self, delta_time_p):
        """
        Update all boid's properties.
        """
        self._update_position(delta_time_p)
    
        self._rotate_shape()
        
        self.position = np.array([self.shape.x,self.shape.y])

        self._edge()

        self._apply_forces(self.nearby_boids)

        self._limit_velocity()



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
    
    def get_nearby_boids(self):
        return self.nearby_boids
    
    def set_size(self,size_p):
        self.size = size_p
    
    def set_color(self, color_p):
        self.color = color_p
    
    def set_velocity(self, velocity_p):
        self.velocity = velocity_p
    
    def set_position(self, position_p):
        self.position = np.array(position_p)
    
    def set_nearby_boids(self, nearby_boids_p):
        self.nearby_boids = nearby_boids_p
    




    
    