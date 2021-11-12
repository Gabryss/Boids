"""
Initialize and start the simulation

1-Initialize the window
2-Initialize graphics batched rendering (for optimized performance)
3-Start the simulation
"""

import pyglet
from enums.config import Config
import boids


window = pyglet.window.Window(
    fullscreen = False,
    resizable = True,
    caption = "Boid simulation",
)

@window.event
def on_draw():
    window.clear()
    Config.BATCH.value.draw()

if __name__ == "__main__":
    # Start it up!
    # init()
    boid = boids.initialize_boids()

    # Update the game 120 times per second
    # pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()