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
from simulate import Simulate


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


if __name__ == "__main__":

    simulation = Simulate()
    simulation.init()

    def update(dt):
        # Update the simulation
        for i in range(len(simulation.boids_list)):
            simulation.boids_list[i].update(dt)
            simulation.get_boids(accuracy="nearby")

    # Update the game 60 times per second
    pyglet.clock.schedule_interval(update, 1 / 60.0)

        

    # Run the app
    pyglet.app.run()