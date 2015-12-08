"""
Created on 1.12.2015

:author: Rene Hollander
"""

import math

from abc import ABCMeta, abstractmethod
from euclid import Vector3
from pyglet.gl import *
from util import auto_str, toGlMatrix
from util.texture import Texture


@auto_str
class Renderer(metaclass=ABCMeta):
    """
    An abstract class that gets inherited from all Renderer
    """

    @abstractmethod
    def draw(self, body, matrix):
        """
        Draw the supplied body with the specified MVP Matrix

        :param body: The body to render
        :type body: :class:`solarsystem.body.Body`
        :param matrix:
        :type matrix: :class:`euclid.Matrix4`
        :return: None
        """

        pass


class BodyRenderer(Renderer):
    """
    Renders the body at a fixed position given by the MVP matrix
    """

    def draw(self, body, matrix):
        matrix.translate(body.xyz.x, body.xyz.y, body.xyz.z)
        matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        matrix.rotate_axis(body.axial_tilt, Vector3(0, 1, 0))
        matrix.rotate_axis(math.radians(-360 * body.timefactor), Vector3(0, 0, 1))
        glLoadMatrixd(toGlMatrix(matrix))
        if body.draw_texture:
            body.texture.draw()
        else:
            glColor3f(body.color["r"] / 255.0, body.color["g"] / 255.0, body.color["b"] / 255.0)

        gluSphere(body.sphere, body.radius, 50, 50)
        glDisable(GL_TEXTURE_2D)


class OrbitingBodyRenderer(BodyRenderer):
    """
    Renders the body at the current position in orbit. If :draw_orbit is true, the orbit will be plotted,
    """

    def draw(self, body, matrix):
        # draw the in the constructor plotted line if requested
        if body.draw_orbit:
            linematrix = matrix.__copy__()
            if body.parent is not None:
                linematrix.translate(body.parent.xyz.x, body.parent.xyz.y, body.parent.xyz.z)

            glLoadMatrixd(toGlMatrix(linematrix))
            glLineWidth(1.25)
            glColor3f(body.color["r"] / 255.0, body.color["g"] / 255.0, body.color["b"] / 255.0)
            body.orbit_line_batch.draw()

        glColor3f(1.0, 1.0, 1.0)

        super().draw(body, matrix)


class OrbitingBodyWithRingRenderer(OrbitingBodyRenderer):
    """
    Renders the body at the current position in orbit. If :draw_orbit is true, the orbit will be plotted,
    The parameters for the rings are set with setup_ring_renderer
    """

    def draw(self, body, mat):
        if body.draw_texture:
            matrix = mat.__copy__()
            matrix.translate(body.xyz.x, body.xyz.y, body.xyz.z)
            matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
            matrix.rotate_axis(body.axial_tilt, Vector3(0, 1, 0))
            glLoadMatrixd(toGlMatrix(matrix))
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_CULL_FACE)
            body.ring_texture.draw()
            gluDisk(body.ring_disk, body.ring_inner_radius, body.ring_outer_radius, 50, 50)
            glEnable(GL_CULL_FACE)
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_TEXTURE_2D)

        super().draw(body, mat)


def setup_ring_renderer(ring_texture_name, ring_inner_radius, ring_outer_radius, body):
    """
    Sets the needed parameters for the OrbitingBodyWithRingRenderer.

    :param ring_texture_name: Name of the texture
    :type ring_texture_name: str
    :param ring_inner_radius: Inner radius of the rings
    :type ring_inner_radius: float
    :param ring_outer_radius: Outer radius of the rings
    :type ring_outer_radius: float
    :param body: Body to apply these parameters to
    :type body: :class:`solarsystem.body.Body`
    :return: Supplied body
    :rtype: :class:`solarsystem.body.Body`
    """

    body.ring_inner_radius = ring_inner_radius
    body.ring_outer_radius = ring_outer_radius
    body.ring_texture = Texture(ring_texture_name)
    body.ring_disk = gluNewQuadric()
    gluQuadricNormals(body.ring_disk, GLU_SMOOTH)
    gluQuadricTexture(body.ring_disk, GL_TRUE)
    return body
