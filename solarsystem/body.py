import math

from abc import ABCMeta, abstractmethod
from euclid import Vector3
from pyglet.gl import *
from pyglet.graphics import Batch
from util.mathhelper import toGlMatrix
from util.texture import Texture


class Body(object, metaclass=ABCMeta):
    def __init__(self, parent, name, color, radius, axial_tilt, sidereal_rotation_period):
        self.parent = parent
        self.name = name
        self.color = color
        self.radius = radius
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period
        self.timefactor = 0
        self.draw_orbit = True
        self.draw_texture = True

        self.texture = Texture(self.name.lower() + ".jpg")
        self.sphere = gluNewQuadric()
        gluQuadricNormals(self.sphere, GLU_SMOOTH)
        gluQuadricTexture(self.sphere, GL_TRUE)

    def update(self, time):
        self.timefactor = (time % self.sidereal_rotation_period) / self.sidereal_rotation_period

    @abstractmethod
    def render(self, matrix):
        matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        matrix.rotate_axis(math.radians(self.axial_tilt), Vector3(0, 1, 0))
        matrix.rotate_axis(math.radians(-360 * self.timefactor), Vector3(0, 0, 1))
        glLoadMatrixd(toGlMatrix(matrix))
        if self.draw_texture:
            self.texture.draw()
        else:
            glColor3f(self.color["r"] / 255.0, self.color["g"] / 255.0, self.color["b"] / 255.0)

        gluSphere(self.sphere, self.radius, 50, 50)
        glDisable(GL_TEXTURE_2D)


class StationaryBody(Body, metaclass=ABCMeta):
    def __init__(self, parent, name, color, radius, axial_tilt, sidereal_rotation_period, xyz=Vector3()):
        super().__init__(parent, name, color, radius, axial_tilt, sidereal_rotation_period)
        self.xyz = xyz

    def render(self, matrix):
        matrix.translate(self.xyz.x, self.xyz.z, self.xyz.y)
        super().render(matrix)


class OrbitingBody(Body, metaclass=ABCMeta):
    def __init__(self, parent, name, color, radius, orbit, axial_tilt, sidereal_rotation_period):
        super().__init__(parent, name, color, radius, axial_tilt, sidereal_rotation_period)
        self.orbit = orbit
        self.orbit_line_batch = Batch()
        self.xyz = Vector3()

        orbit_line = []
        for angle in range(0, 360):
            pos = self.orbit.calculate_by_angle(angle)
            orbit_line.append(pos.x)
            orbit_line.append(pos.y)
            orbit_line.append(pos.z)
        self.orbit_line_batch.add(int(len(orbit_line) / 3), GL_LINES, None, ('v3f', tuple(orbit_line)))

    def update(self, time):
        super().update(time)
        if self.parent is not None:
            self.xyz = self.parent.xyz + self.orbit.calculate(time)
        else:
            self.xyz = self.orbit.calculate(time)

    def render(self, matrix):
        if self.draw_orbit:
            linematrix = matrix.__copy__()
            linematrix.translate(0, 0, 0)
            if self.parent is not None:
                linematrix.translate(self.parent.xyz.x, self.parent.xyz.z, self.parent.xyz.y)
            linematrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))

            glLoadMatrixd(toGlMatrix(linematrix))
            glLineWidth(2)
            glColor3f(1.0, 0.0, 0.0)
            self.orbit_line_batch.draw()

        glColor3f(1.0, 1.0, 1.0)

        matrix.translate(self.xyz.x, self.xyz.z, self.xyz.y)
        super().render(matrix)
