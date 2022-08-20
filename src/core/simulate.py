"""
Simulation file
"""

import boids
from enums.config import Config



class Simulate():

    def __init__(self):
        self.boids_list=[]
        self.width = Config.WINDOW_WIDTH.value
        self.height = Config.WINDOW_HEIGHT.value
    
    def init(self):
        for i in range(int(Config.DEFAULT_BOIDS_NB.value)):
            self.boids_list.append(boids.initialize_boid(Config.WINDOW_WIDTH.value,Config.WINDOW_HEIGHT.value))
    
    def get_boids(self, accuracy):
        if accuracy == 'all':
            for i in range(len(self.boids_list)):
                self.boids_list[i].set_nearby_boids(self.boids_list)
        else:
            for i in range(len(self.boids_list)):
                self.boids_list[i].discover_nearby_boids(self.boids_list)


    def update(self, delta_time):
            """Animate the shapes"""
            self.time += delta_time
            self.square.rotation = self.time * 15