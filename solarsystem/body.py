import math
from abc import ABCMeta
from euclid import Vector3
from pyglet.gl import *
from util.mathhelper import toGlMatrix
from util.texture import Texture


class Body(object, metaclass=ABCMeta):
    def __init__(self, parent):
        self.parent = parent


class Planet(Body, metaclass=ABCMeta):
    def __init__(self, parent, name, orbit, mean_radius, axial_tilt, sidereal_rotation_period):
        super().__init__(parent)

        self.name = name
        self.orbit = orbit
        self.mean_radius = mean_radius
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period

        self.texture = Texture(self.name.lower() + ".jpg")
        self.sphere = gluNewQuadric()
        gluQuadricNormals(self.sphere, GLU_SMOOTH)
        gluQuadricTexture(self.sphere, GL_TRUE)

    def update(self, time):
        self.timefactor = (time % self.sidereal_rotation_period) / self.sidereal_rotation_period
        if self.parent is not None:
            self.xyz = self.parent.xyz + self.orbit.calculate(time)
        else:
            self.xyz = self.orbit.calculate(time)

    def render(self, matrix):
        # matrix.translate(0, 0, -20)
        matrix.translate(self.xyz.x, self.xyz.z, self.xyz.y)
        matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        matrix.rotate_axis(math.radians(self.axial_tilt), Vector3(0, 1, 0))
        matrix.rotate_axis(math.radians(-360 * self.timefactor), Vector3(0, 0, 1))
        glLoadMatrixd(toGlMatrix(matrix))
        self.texture.draw()
        gluSphere(self.sphere, self.mean_radius, 50, 50)
        glDisable(GL_TEXTURE_2D)

    def __str__(self):
        return self.name + "({orbit: " + str(self.orbit) + ", mean_radius: \"" + str(
            self.mean_radius) + "\", axial_tilt: \"" + str(self.axial_tilt) + "\", sidereal_rotation_period: \"" + str(
            self.sidereal_rotation_period) + "})"
