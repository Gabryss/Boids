"""
Config file for setup the simulation

Properties of all forces and boid population/group
"""
from enum import Enum
from .colors import Color
import pyglet

class Config (Enum):
    DEFAULT_REPULSION_FORCE = 5.0 # repulsion must be important compared to cohesion
    DEFAULT_SEPARATION_FORCE = 1.0
    DEFAULT_COHESION_FORCE = 0.0001
    DEFAULT_ALIGNMENT_FORCE = 1.0

    DEFAULT_REPULSION_DIST = 100.0
    DEFAULT_SEPARATION_DIST = 10.0 # no need to get a large range to compute separation, if max speed is increasing you may extend a bit this range
    DEFAULT_COHESION_DIST = 100
    DEFAULT_ALIGNMENT_DIST = 100.0

    DEFAULT_BOIDS_NB = 10

    DEFAULT_COLOR_RED = Color.RED.value
    DEFAULT_COLOR_BLUE = Color.BLUE.value
    DEFAULT_COLOR_GREEN = Color.GREEN.value
    DEFAULT_COLOR_PURPLE = Color.PURPLE.value
    MAXSPEED = 100.0
    MAXFORCE = 10.0
    VISIBLE_ANGLE = 90.0
    MASS = 1

    COHESION_ON = True
    REPULSION_ON = True
    ALIGNMENT_ON = True
    SEPARATION_ON = True

    COHESION_OFF = False
    REPULSION_OFF = False
    ALIGNMENT_OFF = False
    SEPARATION_OFF = False

    BATCH = pyglet.graphics.Batch()