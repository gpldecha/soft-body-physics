# Particle.py
# Created by Michael Marek (2015)
# A single point whose motion is simulated through space. Each particle is simulated using a
# Verlet integration method; each particle contains a reference to it's current position and it's
# position relative to the last time step. Velocity is implicitly claculated with direction and
# magnitude as the difference between this particle's current and previous position.


import math

from Vector import *
from Material import *
from Colisions import *

class Particle:
    #
    material     = None              # particle material
    world        = None              # world particle is simulated in
    position     = Vector(0.0, 0.0)  # current position
    previous     = Vector(0.0, 0.0)  # previous time-step [t-dt] position
    velocity     = Vector(0.0, 0.0)  # [readme] particle velocity
    acceleration = Vector(0.0, 0.0)  # acceleration of the particle
    contact      = None

    # Class constructor. Initialize the particle within the simulation world.
    #
    # @param    world       reference to the simulation world this particle resides in
    # @param    x           particle horizontal position relative to the world
    # @param    y           particle vertical position relative to the world
    # @param    material    specify this particle's material; default if none provided
    # @return   null
    #
    def __init__(self, world, x=0.0, y=0.0, material=None):
        self.world    = world
        self.position = Vector(x, y)
        self.previous = Vector(x, y)
        self.contact = None
        if material == None:
            self.material = Material()
        else:
            self.material = material
        self.is_in_contact = False


    # Simulate this particle's motion. A mass of zero denotes that the particle is 'pinned', and
    # cannot move.
    #
    # @param    null
    # @param    null
    #
    def Simulate(self):
        if not self.material.mass:
            return
        self.velocity = 2.0 * self.position - self.previous
        self.previous = self.position
        self.position = self.velocity + self.acceleration * self.world.delta**2.0
        self.velocity = self.position - self.previous
        self.acceleration = Vector.zero()


    # Accelerate this particle. This method affects the particle's acceleration, disregarding mass.
    # Use this if you need to immediately affect the particle's acceleration.
    #
    # @param    rate    applied acceleration (m/s^2)
    # @return   null
    #
    def Accelerate(self, rate):
        self.acceleration += rate


    # Apply a force to this particle. This method affect's the particle's acceleration, taking it's
    # mass into account. To move an object, a large enough force must be applied to immediately
    # move it, or a smaller force over time must be applied.
    #
    # @param    force   force applied to the particle (N)
    # @return   null
    #
    def ApplyForce(self, force):
        if self.material.mass != 0.0:
            self.acceleration += force / self.material.mass


    # Apply an impulse to this particle. This method affect's the particle's velocity, taking it's
    # mass into account. Since the particle is simulated via Verlet integration, a change in the
    # particle's position results in an immediate change in velocity. Use this method to
    # immediately affect the particle's velocity.
    #
    # @param    impulse     impulse directly applied to the particle (a*dt / m)
    def ApplyImpulse(self, impulse):
        if self.material.mass != 0.0:
            self.position += impulse / self.material.mass


    # Set the acceleration of this particle to zero. By applying forces and resetting them after,
    # we ensure that the forces must be applied every time step of the simulation in order to be
    # regarded as a continuous force.
    #
    # @param    null
    # @return   null
    #
    def ResetForces(self):
        self.acceleration = Vector.zero()


    # Restrain this particle to the simulation world boundaries. If a particle exceeds the world
    # boundaries, we bounce it back into the world. We do this by correcting the particle's current
    # position to the boundary line, and adjust the previous position so that next time step the
    # particle maintains a velocity that is accurate as such the particle takes into account
    # restitution and friction.
    #
    # @param    null
    # @return   null
    #
    def Restrain(self):
        #
        # screen boundaries
        self.is_in_contact = False
        if update_particle(self.position, self.previous, self.material, self.world.boundary_x, self.world.boundary_y):
            self.is_in_contact = True
            self.contact = Vector(self.position.x, self.position.y)
        if self.world.manipulator.update_particle(self):
            self.is_in_contact = True
            self.contact = Vector(self.position.x, self.position.y)
