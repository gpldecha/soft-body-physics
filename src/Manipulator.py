from Vector import *
import pygame as game


class Manipulator:

    def __init__(self, position, direction, length, width):
        self.position = position
        self.direction = direction
        self.length = length
        self.width = width

    def update_particle(self, particle):
        # convert particle to frame of reference of manipulator
        pass

    def render(self, screen, world_to_pixel):
        pos1 = self.position - Vector(self.length/2, self.width/2)
        pos2 = self.position - Vector(self.length/2, -self.width/2)
        pos3 = self.position - Vector(-self.length/2, -self.width/2)
        pos4 = self.position - Vector(-self.length/2, self.width/2)

        pos1 = world_to_pixel(pos1)
        pos2 = world_to_pixel(pos2)
        pos3 = world_to_pixel(pos3)
        pos4 = world_to_pixel(pos4)

        game.draw.line(screen, (255, 0, 0), pos1, pos2, 1)
        game.draw.line(screen, (255, 0, 0), pos2, pos3, 1)
        game.draw.line(screen, (255, 0, 0), pos3, pos4, 1)
        game.draw.line(screen, (255, 0, 0), pos4, pos1, 1)

