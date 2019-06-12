from Vector import *
import pygame as game
import numpy as np
from Colisions import *


class Manipulator:

    def __init__(self, position, orientation, length, width):
        self.translation = np.array([position.x, position.y])
        self.orientation = orientation
        self.length = length  # y
        self.width = width  # x

        self.boundary_x = [-self.width/2., self.width/2.0]
        self.boundary_y = [-self.length/2., self.length/2.0]
        self.R = np.array([[np.cos(orientation), -np.sin(orientation)], [np.sin(orientation), np.cos(orientation)]])

    def move(self, dx, dy):
        self.translation[0] += dx
        self.translation[1] += dy

    def update_particle(self, particle):
        # convert particle to frame of reference of manipulator
        position_frame_manipulator = self._to_manipulator_frame(np.array([particle.position.x, particle.position.y]))
        if self.is_in(position_frame_manipulator):
            previous_frame_manipulator = self._to_manipulator_frame(np.array([particle.previous.x, particle.previous.y]))
            update_particle_manipulator(position_frame_manipulator, previous_frame_manipulator, particle.material, self.boundary_x, self.boundary_y)
            position = self._to_world_frame(position_frame_manipulator)
            previous = self._to_world_frame(previous_frame_manipulator)
            particle.position.x = position[0]
            particle.position.y = position[1]
            particle.previous.x = previous[0]
            particle.previous.y = previous[1]
            return True
        return False

    def is_in(self, point):
        if (point[0] < self.width/2.) and (point[0] > -self.width/2.) and (point[1] < self.length/2.) and (point[1] > -self.length/2.):
            return True
        return False

    def _to_manipulator_frame(self, p):
        return np.dot(np.transpose(self.R), p) - np.dot(np.transpose(self.R), self.translation)

    def _to_world_frame(self, p):
        return np.dot(self.R, p) + self.translation

    def render(self, screen, world_to_pixel):
        pos1 = self.translation - np.array([ self.length/2.,  self.width/2.])
        pos2 = self.translation - np.array([ self.length/2., -self.width/2.])
        pos3 = self.translation - np.array([-self.length/2., -self.width/2.])
        pos4 = self.translation - np.array([-self.length/2.,  self.width/2.])

        pos1 = world_to_pixel(pos1)
        pos2 = world_to_pixel(pos2)
        pos3 = world_to_pixel(pos3)
        pos4 = world_to_pixel(pos4)

        game.draw.line(screen, (255, 0, 0), pos1, pos2, 1)
        game.draw.line(screen, (255, 0, 0), pos2, pos3, 1)
        game.draw.line(screen, (255, 0, 0), pos3, pos4, 1)
        game.draw.line(screen, (255, 0, 0), pos4, pos1, 1)

