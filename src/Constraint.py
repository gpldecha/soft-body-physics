# Constraint.py
# Created by Michael Marek (2015)
# Creates a constraint between two particles in the simulation world. Once the constraint is
# created and two points are specified, the constraint attempts to maintain that initial distance
# between the two particles. The constraint is modelled as a spring, and as such, is mathematically
# defined using Hooke's law. If the particle's become too close or two far apart, a force is
# applied to each in order to restore the distance equilibrium. For our purposes, since we model
# the motion of particles using Verlet integration, we directly adjust the impulse of the
# particles to move them, rather than apply a force.


import math

from Vector import *
from Particle import *
import numpy as np


class Constraint:
    #
    node1  = None   # first constrained particle
    node2  = None   # second constrained particle
    target = 0.0    # target distance the particles try to maintain from one another
    stiff  = 1.0    # Hooke's law spring constant [0.0, 1.0] (0 = no spring, 1 = rigid bar)
    damp   = 0.0    # Hooke's law dampening constant


    # Class constructor. Grab references of the two constrained particles, get a specified spring
    # constant for the constraint, and establish a target distance between the particles.
    #
    # @param    p1  first particle constrained
    # @param    p2  second particle constrained
    # @param    s   spring constant [0.0, 1.0]
    # @param    d   distance constraint (default seprerating distance)
    # @return   null
    #
    def __init__(self, p1, p2, s, is_membrane):
        #
        self.node1  = p1
        self.node2  = p2
        self.stiff  = s
        self.target = math.sqrt((p2.position.x - p1.position.x)**2 + (p2.position.y - p1.position.y)**2)
        self.is_membrane = is_membrane


    # Attempt to maintain the target distance between the two constrained particles. Calculate the
    # distance between the two particles and apply a restoring impulse to each particle.
    #
    # @param    null
    # @return   null
    #
    def Relax(self):
        #

        D = self.node2.position - self.node1.position
        F = 0.5 * self.stiff * (D.length() - self.target) * D.normalized()
        if self.node1.is_in_contact and self.node2.is_in_contact and not self.is_membrane:
            # print('both in contact')
            self.node1.position = self.node1.contact
            self.node2.position = self.node2.contact

            direction = self.node1.position - self.node2.position
            distance = np.sqrt(direction[0] ** 2 + direction[1] ** 2)
            direction.normalize()
            delta = distance
            self.target = delta
            return

        if self.node1.material.mass != 0.0 and not self.node2.material.mass:
            self.node1.ApplyImpulse(2.0 * +F)
            self.node1.ApplyForce(2.0 * +F)
        elif not self.node1.material.mass and self.node2.material.mass != 0.0:
            self.node2.ApplyImpulse(2.0 * -F)
            self.node2.ApplyForce(2.0 * -F)
        else:
            self.node1.ApplyImpulse(+F)
            self.node2.ApplyImpulse(-F)

    def RelaxNoForce(self):

        if self.is_membrane:
            self._relax_membrane()
        else:
            self._relax_link()

    def _relax_membrane(self):
        direction_node_12 = self.node2.position - self.node1.position
        direction_node_21 = self.node1.position - self.node2.position
        current_length = np.sqrt(direction_node_12[0] ** 2 + direction_node_12[1] ** 2)
        direction_node_12.normalize()
        direction_node_21.normalize()

        delta = (self.target - current_length)/2.0
        self.node2.position[0] = self.node2.position[0] + direction_node_12[0]*delta
        self.node2.position[0] = self.node2.position[0] + direction_node_12[0]*delta

        self.node1.position[0] = self.node1.position[0] + direction_node_21[0]*delta
        self.node1.position[0] = self.node1.position[0] + direction_node_21[0]*delta

    def _relax_link(self):

        if self.node1.is_in_contact and not self.node2.is_in_contact:
            direction = self.node2.position - self.node1.position
            current_length = np.sqrt(direction[0]**2 + direction[1]**2)
            direction.normalize()
            delta = self.target - current_length
            k = 0.025
            self.node2.position[0] = self.node2.position[0] + k*direction[0]*delta
            self.node2.position[1] = self.node2.position[1] + k*direction[1]*delta

            self.node2.previous[0] = self.node2.previous[0] + k*direction[0]*delta
            self.node2.previous[1] = self.node2.previous[1] + k*direction[1]*delta

        elif not self.node1.is_in_contact and self.node2.is_in_contact:
            direction = self.node1.position - self.node2.position
            distance = np.sqrt(direction[0]**2 + direction[1]**2)
            direction.normalize()
            delta = self.target - distance
            k = 0.025
            self.node1.position[0] = self.node1.position[0] + k*direction[0]*delta
            self.node1.position[1] = self.node1.position[1] + k*direction[1]*delta

            self.node1.previous[0] = self.node1.previous[0] + k*direction[0]*delta
            self.node1.previous[1] = self.node1.previous[1] + k*direction[1]*delta

        elif self.node1.is_in_contact and self.node2.is_in_contact:
            print('both constraints in contact')
