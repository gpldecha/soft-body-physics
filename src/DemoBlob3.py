import math
import pygame as game

from App import *
from VerletPhysics import *
from Manipulator import Manipulator


def pixel_to_world(pixel, world):
    # i,j => x, y
    return 2.0*pixel.x/(2.0*world.hsize.x) - 1.0, -(float(pixel.y)/world.hsize.y - 1.0)


def world_to_pixel(position, world):
    return int((position.x + 1.0)*(2.0*world.hsize.x)/2.0), int((position.y + 1.0)*world.hsize.y)


class DemoBlob(App):
    #
    world    = World(Vector(600.0, 600.0), Vector(0, 2), 6)
    blob     = world.AddComposite()
    blobsize = 0.25
    #
    grabbed  = None
    radius   = 20
    strength = 0.10

    #
    def Initialize(self):
        #
        k = 0.8
        steps = 40

        #
        # @param    f   coefficient of friction [0.0, 1.0]
        # @param    b   coefficient of restitution [0.0, 1.0]
        mat = Material(1.0, 0.2, 0.9)
        self.world.gravity = Vector(0., 0.)
        self.manipulator = Manipulator(position=Vector(0, -0.5), direction=Vector(0, 1), length=0.6, width=0.2)

        outer = []
        kinex = []

        # outer skin
        for i in range(steps):
            x = self.blobsize * math.cos(i * (2.0 * math.pi) / steps)
            y = self.blobsize * math.sin(i * (2.0 * math.pi) / steps)
            outer.append(self.world.AddParticle(x, y, mat))

        # connect outer skin
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(outer[i-1], outer[i], k))
        kinex.append(self.world.AddConstraint(outer[len(outer)-1], outer[0], k))
        for i in range(steps / 2):
            to = i + steps / 2
            if to >= steps:
                to -= steps
            kinex.append(self.world.AddConstraint(outer[i], outer[to], k))

        self.blob.AddParticles(outer)
        self.blob.AddConstraints(kinex)

    #
    def Update(self):
        if game.mouse.get_pressed()[0]:
            if self.grabbed == None:
                closest = self.ClosestPoint()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed != None:
                mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
                xy = pixel_to_world(mouse, self.world)
                mouse = Vector(xy[0], xy[1])
                force = (mouse - self.grabbed.position) * self.strength
                self.grabbed.ApplyImpulse(force)
        else:
            self.grabbed = None

        if game.key.get_pressed()[game.K_ESCAPE]:
            self.Exit()
        self.world.Simulate()

    #
    def Render(self):
        #
        self.screen.fill((24, 24, 24))
        for c in self.world.constraints:
            pos1 = world_to_pixel(c.node1.position, self.world)
            pos2 = world_to_pixel(c.node2.position, self.world)
            game.draw.line(self.screen, (255, 255, 255), pos1, pos2, 1)
        for p in self.world.particles:
            pos = world_to_pixel(p.position, self.world)
            game.draw.circle(self.screen, (255, 255, 255), pos, 2, 0)

        pos = world_to_pixel(Vector(-1, 1), self.world)
        game.draw.circle(self.screen, (255, 0, 0), pos, 10, 0)

        self.manipulator.render(self.screen, lambda pos: world_to_pixel(pos, self.world))

        game.display.update()

    #
    def ClosestPoint(self):
        mouse    = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        print('mouse {} {}'.format(mouse.x, mouse.y))
        xy = pixel_to_world(mouse, self.world)
        mouse = Vector(xy[0], xy[1])
        print(xy)
        closest  = None
        distance = float('inf')
        for particle in self.world.particles:
            d = mouse.distance(particle.position)
            if d < distance:
                closest  = particle
                distance = d
        return (closest, distance)


if __name__ == "__main__":
    print "Starting..."
    app = DemoBlob("Loco Roco", 600, 600, 30)
    app.Run()
    print "Ending..."
