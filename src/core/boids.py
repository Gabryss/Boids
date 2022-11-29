"""
Boids core file
"""
from enums.config import Config
import random
import pyglet
import numpy as np
import rules
import utils

def initialize_boid(width, height):
    return(Boid(position_p=[random.uniform(0,width), random.uniform(0,height)], velocity_p=[random.uniform(-Config.MAXSPEED.value,Config.MAXSPEED.value), random.uniform(-Config.MAXSPEED.value,Config.MAXSPEED.value)]))


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
        #Boid shape parameters : center_point [x1,y1], lower_wing [x2,y2], noze [x3,y3], upper_wing[x4,y4], color, batch
        self.shape = pyglet.shapes.Polygon(self.bounds[0],self.bounds[1],self.bounds[2],self.bounds[3],color=self.color, batch=Config.BATCH.value)
        self.shape.x = self.position[0]
        self.shape.y = self.position[1]
        self.shape.rotation = random.uniform(0,360)


    
    
    def discover_nearby_boids(self,boids):
        """
        Discover nearby boids.
        """
        nearby_boids = []
        for boid in boids:
            diff = [other_boid - this_boid for other_boid, this_boid in zip(boid.get_position(), self.position)]

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



    def distance_boids(self, boids):
        """
        Calculate the distance between boids.
        """
        for boid in boids:
            if boid != self:
                distance = np.linalg.norm(boid.get_position() - self.position)
                if distance <= Config.MAXDIST.value:
                    self.nearby_boids.append(boid)
        return self.nearby_boids
    
    def _can_see(self, boid):
        """
        Check if the boid can see another boid.
        """
        diff = boid.get_position() - self.position
        return (boid != self and
                np.linalg.norm(diff) <= Config.MAXDIST.value and
                utils.angle_between(self.velocity, diff) <= Config.VISIBLE_ANGLE.value)

    
    def _rotate_shape(self):
        """
        Rotate base image using the velocity and assign to image.
        """
        # angle = -np.rad2deg(np.angle(self.velocity[0] + 1j * self.velocity[1]))
        angle = -np.rad2deg(np.arctan2(self.velocity[1], self.velocity[0]))

        self.shape.rotation = angle


    def _edge(self):
        """
        Check if the boid is outside the window and if so, reflect it.
        If the boid touch a border of the window, it will bounce on it.
        """       
        if self.shape.position[0] >= Config.WINDOW_WIDTH.value:
            self.shape.position = Config.WINDOW_WIDTH.value, self.shape.position[1]
            self.velocity = -self.velocity
            self.acceleration = -self.acceleration
        
        if self.shape.position[1] <= 0:
            self.shape.position = self.shape.position[0], 0
            self.velocity = -self.velocity
            self.acceleration = -self.acceleration

        if self.shape.position[1] >= Config.WINDOW_HEIGHT.value:
            self.shape.position = self.shape.position[0], Config.WINDOW_HEIGHT.value
            self.velocity = -self.velocity
            self.acceleration = -self.acceleration

        
        if self.shape.position[0] <= 0:
            self.shape.position = 0, self.shape.position[1]
            self.velocity = -self.velocity
            self.acceleration = -self.acceleration
    

    def _apply_forces(self, boids):
        """
        Apply the forces to the boid.
        """
        alignment_vector = rules.alignment(self,boids)
        cohesion_vector = rules.cohesion(self,boids)
        separation_vector = rules.separation(self,boids)
        centripete_vector = rules.centripete(self)
        self.forces = [ 
                        (Config.DEFAULT_ALIGNMENT_FORCE.value, alignment_vector),
                        (Config.DEFAULT_COHESION_FORCE.value, cohesion_vector),
                        (Config.DEFAULT_SEPARATION_FORCE.value, separation_vector),
                        # (0.02, centripete_vector),
                        ]
        
        for force, vector in self.forces:
            if force and vector is not None:
                self.acceleration += vector * force

        self.velocity += self.acceleration * self.time
        

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
        self.time = delta_time_p
        self.shape.x += self.velocity[0] * delta_time_p
        self.shape.y += self.velocity[1] * delta_time_p

        

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

        self.position = np.array([self.shape.x,self.shape.y])




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
    




    
    