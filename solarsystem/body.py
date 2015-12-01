"""
Created on 03.11.2015

:author: Rene Hollander
"""

from abc import ABCMeta, abstractmethod
from euclid import Vector3
from pyglet.gl import *
from pyglet.graphics import Batch
from solarsystem.renderer import BodyRenderer, OrbitingBodyRenderer
from util.texture import Texture


class Body(object, metaclass=ABCMeta):
    """
    An abstract class defining an body in the solarsystem
    """

    def __init__(self, parent, name, texturename, color, radius, axial_tilt, sidereal_rotation_period, renderer=BodyRenderer()):
        """
        Creates a new body with the given parameters

        :param parent: Parent body in the system
        :type parent: :class:`Body`
        :param name: Name of the body
        :type name: str
        :param texturename: Name of the texture
        :type texturename: str
        :param color: Dictionary with r, g and b values
        :type color: dict
        :param radius: Radius of the body
        :type radius: float
        :param axial_tilt: Axial Tilt in degrees
        :type axial_tilt: float
        :param sidereal_rotation_period: Rotation period (siderial) around its own axis
        :type sidereal_rotation_period: float
        """

        self.xyz = Vector3()
        self.parent = parent
        self.name = name
        self.texturename = texturename
        self.color = color
        self.radius = radius
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period
        self.timefactor = 0
        self.draw_orbit = True
        self.draw_texture = True
        self.renderer = renderer

        self.texture = Texture(texturename)
        self.sphere = gluNewQuadric()
        gluQuadricNormals(self.sphere, GLU_SMOOTH)
        gluQuadricTexture(self.sphere, GL_TRUE)

    def update(self, time):
        """
        Update the body (Calculate current orbit position)

        :param time: Delta Time
        :type time: float
        """

        self.timefactor = (time % self.sidereal_rotation_period) / self.sidereal_rotation_period

    @abstractmethod
    def draw(self, matrix):
        """
        Draw the body

        :param matrix: Current Model-View-Projection matrix
        :type matrix: :class:`euclid.Matrix4`
        """

        self.renderer.draw(self, matrix)


class StationaryBody(Body, metaclass=ABCMeta):
    """
    A stationary body in the solarsystem (Body without an orbit)
    """

    def __init__(self, parent, name, texturename, color, radius, axial_tilt, sidereal_rotation_period, xyz=Vector3()):
        """
        Creates a new body with the given parameters

        :param parent: Parent body in the system, None if it doesn't have one
        :type parent: None, :class:`Body`
        :param name: Name of the body
        :type name: str
        :param texturename: Name of the texture
        :type texturename: str
        :param color: Dictionary with r, g and b values
        :type color: dict
        :param radius: Radius of the body
        :type radius: float
        :param axial_tilt: Axial Tilt in degrees
        :type axial_tilt: float
        :param sidereal_rotation_period: Rotation period (siderial) around its own axis
        :type sidereal_rotation_period: float
        :param xyz: Position of the object, default 0, 0, 0
        :type xyz: :class:`euclid.Vector3`
        """

        super().__init__(parent, name, texturename, color, radius, axial_tilt, sidereal_rotation_period)
        self.xyz = xyz

    def draw(self, matrix):
        """
        Draw the body

        :param matrix: Current Model-View-Projection matrix
        :type matrix: :class:`euclid.Matrix4`
        """

        matrix.translate(self.xyz.x, self.xyz.z, self.xyz.y)
        super().draw(matrix)


class OrbitingBody(Body, metaclass=ABCMeta):
    """
    An orbiting body in the solarsystem
    """

    def __init__(self, parent, name, texturename, color, radius, orbit, axial_tilt, sidereal_rotation_period, renderer=OrbitingBodyRenderer()):
        """
        Creates a new body with the given parameters

        :param parent: Parent body in the system
        :type parent: :class:`Body`
        :param name: Name of the body
        :type name: str
        :param texturename: Name of the texture
        :type texturename: str
        :param color: Dictionary with r, g and b values
        :type color: dict
        :param radius: Radius of the body
        :type radius: float
        :param orbit: Orbit of the body
        :type orbit: :class:`solarsystem.orbit.Orbit`
        :param axial_tilt: Axial Tilt in degrees
        :type axial_tilt: float
        :param sidereal_rotation_period: Rotation period (siderial) around its own axis
        :type sidereal_rotation_period: float
        """

        super().__init__(parent, name, texturename, color, radius, axial_tilt, sidereal_rotation_period, renderer=renderer)
        self.orbit = orbit
        self.orbit_line_batch = Batch()

        # Plot the orbit to a pyglet batch for faster drawing
        orbit_line = []
        for angle in range(0, 360):
            pos = self.orbit.calculate_by_angle(angle)
            orbit_line.append(pos.x)
            orbit_line.append(pos.y)
            orbit_line.append(pos.z)
        self.orbit_line_batch.add(int(len(orbit_line) / 3), GL_LINES, None, ('v3f', tuple(orbit_line)))

    def update(self, time):
        """
        Update the body (Calculate current orbit position)

        :param time: Delta Time
        :type time: float
        """

        super().update(time)
        if self.parent is not None:
            # if this body has an parent, offset the position of this body by the orbit of the parent
            self.xyz = self.parent.xyz + self.orbit.calculate(time)
        else:
            self.xyz = self.orbit.calculate(time)

    def draw(self, matrix):
        """
        Draw the body

        :param matrix: Current Model-View-Projection matrix
        :type matrix: :class:`euclid.Matrix4`
        """

        self.renderer.draw(self, matrix)
