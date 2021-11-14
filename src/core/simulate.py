"""
Simulation file
"""

import boids



def update(self, delta_time):
        """Animate the shapes"""
        self.time += delta_time
        self.square.rotation = self.time * 15