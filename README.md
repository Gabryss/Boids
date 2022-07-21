# Overview
Boids could be related to artificial intelligence entities with simple rules. Each entity does not has proper intelligence but within a group swarm intelligence highlights interesting behaviors.

The name "boid" corresponds to a shortened version of "bird-oid object", which refers to a bird-like object. 🐣

Boids model could be easily seen as bird or fish group behaviors but it is also used in grass movement simulation.

# Behaviors
In order to reproduce the behaviors of birds in groups, three rules have to be implemented.

## Alignment
Steer towards the average heading of local flockmates.
Birds try to change their position so that it corresponds with the average alignment of other nearby birds.
![Alignment](img/Rule_alignment.gif)

## Cohesion
Steer to move towards the average position (center of mass) of local flockmates.
Every bird attempts to move towards the average position of other nearby birds.
![Cohesion](img/Rule_cohesion.gif)

## Separation
Steer to avoid crowding local flockmates.
Each bird attempts to maintain a reasonable amount of distance between itself and any nearby birds, to prevent overcrowding.
![Separation](img/Rule_separation.gif)

# Setup

## Requirements
- Python >= 3.8
- numpy >= 1.21.4
- pyglet >= 1.5.21
