"""
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
from enums.config import Config
import boids


window = pyglet.window.Window(
    fullscreen = True,
    resizable = True,
    caption = "Boid simulation",
)

@window.event
def on_draw():
    window.clear()
    Config.BATCH.value.draw()


if __name__ == "__main__":

    # Initialize all boids!
    boids_list=[]
    for i in range(int(Config.DEFAULT_BOIDS_NB.value)):
        boids_list.append(boids.initialize_boid(window.width,window.height))
        print(boids_list[i].velocity)

    # for i in range(len(boids_list)):
    #     boids_list[i].get_all_boids(boids_list)

    def update(dt):
        for i in range(len(boids_list)):
            boids_list[i].update(dt)
            boids_list[i].get_all_boids(boids_list)

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Run the app
    pyglet.app.run()