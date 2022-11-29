"""
Simulation file

Initialize and start the simulation

1-Initialize the window
2-Initialize graphics batched rendering (for optimized performance)
3-Start the simulation




##TO DO
    -Update window width and height when resized
    -Boids rules
    -Nearby boids detection
    -Walls
    -Translation without changing the pyglet library
    -GUI
"""
import pyglet
import boids
from enums.config import Config



""" 
Initialize the window
"""

window = pyglet.window.Window(
            fullscreen = False,
            height = Config.WINDOW_HEIGHT.value,
            width = Config.WINDOW_WIDTH.value,
            resizable = True,
            caption = "Boid simulation",
        )
batch = Config.BATCH.value

@window.event
def on_draw():
    window.clear()
    batch.draw()




"""
Start the simulation
"""


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





if __name__ == "__main__":

    simulation = Simulate()
    simulation.init()

    def update(dt):
        # Update the simulation
        for i in range(len(simulation.boids_list)):
            simulation.boids_list[i].update(dt)
        for i in range(len(simulation.boids_list)):
            simulation.get_boids(accuracy="nearby")

    # Update the game 60 times per second
    # pyglet.clock.schedule_interval(update, 1 / 30.0)
    pyglet.clock.schedule(update)
        

    # Run the app
    pyglet.app.run()