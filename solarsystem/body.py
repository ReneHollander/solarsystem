import math
from abc import ABCMeta, abstractmethod

from euclid import Vector3
from pyglet.gl import *

from util.mathhelper import toGlMatrix
from util.texture import Texture


class Body(object, metaclass=ABCMeta):
    def __init__(self, parent, name, radius):
        self.parent = parent
        self.name = name
        self.radius = radius

        self.texture = Texture(self.name.lower() + ".jpg")
        self.sphere = gluNewQuadric()
        gluQuadricNormals(self.sphere, GLU_SMOOTH)
        gluQuadricTexture(self.sphere, GL_TRUE)

    def update(self, time):
        pass

    @abstractmethod
    def render(self, matrix):
        pass


class StationaryBody(Body, metaclass=ABCMeta):
    def __init__(self, parent, name, radius, xyz=Vector3()):
        super().__init__(parent, name, radius)
        self.xyz = xyz

    def render(self, matrix):
        matrix.translate(self.xyz.x, self.xyz.z, self.xyz.y)
        glLoadMatrixd(toGlMatrix(matrix))
        self.texture.draw()
        gluSphere(self.sphere, self.radius, 50, 50)
        glDisable(GL_TEXTURE_2D)


class OrbitingBody(Body, metaclass=ABCMeta):
    def __init__(self, parent, name, radius, orbit, axial_tilt, sidereal_rotation_period):
        super().__init__(parent, name, radius)
        self.orbit = orbit
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period

    def update(self, time):
        self.timefactor = (time % self.sidereal_rotation_period) / self.sidereal_rotation_period
        if self.parent is not None:
            self.xyz = self.parent.xyz + self.orbit.calculate(time)
        else:
            self.xyz = self.orbit.calculate(time)

    def render(self, matrix):
        matrix.translate(self.xyz.x, self.xyz.z, self.xyz.y)
        matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        matrix.rotate_axis(math.radians(self.axial_tilt), Vector3(0, 1, 0))
        matrix.rotate_axis(math.radians(-360 * self.timefactor), Vector3(0, 0, 1))
        glLoadMatrixd(toGlMatrix(matrix))
        self.texture.draw()
        gluSphere(self.sphere, self.radius, 50, 50)
        glDisable(GL_TEXTURE_2D)
