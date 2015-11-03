from abc import ABCMeta, abstractmethod
from pywavefront import Wavefront
from pyglet.gl import *


class Planet(object, metaclass=ABCMeta):
    def __init__(self, orbit, mean_radius, axial_tilt, sidereal_rotation_period):
        self.name = self.__class__.__name__
        self.orbit = orbit
        self.mean_radius = mean_radius
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period

        self.obj = Wavefront(self.name.lower() + ".obj")

    def update(self, time):
        self.timefactor = (time % self.sidereal_rotation_period) / self.sidereal_rotation_period

    def render(self):
        glPushMatrix()
        glRotatef(-90 - self.axial_tilt, 0, 0, 1)
        glRotatef(-360 * self.timefactor, 1, 0, 0)
        glRotatef(90, 0, 0, 1)
        glRotatef(0, 0, 1, 0)
        self.obj.draw()
        glPopMatrix()

    def __str__(self):
        return self.name + "({orbit: " + str(self.orbit) + ", mean_radius: \"" + str(
            self.mean_radius) + "\", axial_tilt: \"" + str(self.axial_tilt) + "\", sidereal_rotation_period: \"" + str(
            self.sidereal_rotation_period) + "\"obj: \"" + str(self.obj) + "\"})"
