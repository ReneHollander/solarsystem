import math

from abc import ABCMeta, abstractmethod
from euclid import Vector3
from pyglet.gl import *
from util.mathhelper import toGlMatrix
from util.texture import Texture


class Renderer(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, body, matrix):
        pass


class BodyRenderer(Renderer):
    def draw(self, body, matrix):
        matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        matrix.rotate_axis(math.radians(body.axial_tilt), Vector3(0, 1, 0))
        matrix.rotate_axis(math.radians(-360 * body.timefactor), Vector3(0, 0, 1))
        glLoadMatrixd(toGlMatrix(matrix))
        if body.draw_texture:
            body.texture.draw()
        else:
            glColor3f(body.color["r"] / 255.0, body.color["g"] / 255.0, body.color["b"] / 255.0)

        gluSphere(body.sphere, body.radius, 50, 50)
        glDisable(GL_TEXTURE_2D)


class OrbitingBodyRenderer(BodyRenderer):
    def draw(self, body, matrix):
        # draw the in the constructor plotted line if requested
        if body.draw_orbit:
            linematrix = matrix.__copy__()
            linematrix.translate(0, 0, 0)
            if body.parent is not None:
                linematrix.translate(body.parent.xyz.x, body.parent.xyz.z, body.parent.xyz.y)
            linematrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))

            glLoadMatrixd(toGlMatrix(linematrix))
            glLineWidth(1.25)
            glColor3f(body.color["r"] / 255.0, body.color["g"] / 255.0, body.color["b"] / 255.0)
            body.orbit_line_batch.draw()

        glColor3f(1.0, 1.0, 1.0)

        matrix.translate(body.xyz.x, body.xyz.z, body.xyz.y)
        super().draw(body, matrix)


class OrbitingBodyWithRingRenderer(OrbitingBodyRenderer):
    def draw(self, body, mat):
        matrix = mat.__copy__()
        matrix.translate(body.xyz.x, body.xyz.z, body.xyz.y)
        matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        matrix.rotate_axis(math.radians(body.axial_tilt), Vector3(0, 1, 0))
        glLoadMatrixd(toGlMatrix(matrix))
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        body.ring_texture.draw()
        gluDisk(body.ring_disk, body.ring_inner_size, body.ring_outer_size, 50, 50)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)

        super().draw(body, mat)


def setup_ring_renderer(ring_inner_size, ring_outer_size, body):
    body.ring_inner_size = ring_inner_size
    body.ring_outer_size = ring_outer_size
    body.ring_texture = Texture(body.name + "_ring" + ".png")
    body.ring_disk = gluNewQuadric()
    gluQuadricNormals(body.ring_disk, GLU_SMOOTH)
    gluQuadricTexture(body.ring_disk, GL_TRUE)
    return body
