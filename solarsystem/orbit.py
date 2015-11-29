"""
Created on 03.11.2015

:author: Rene Hollander
"""

from math import sin, cos, radians

from abc import ABCMeta, abstractmethod
from euclid import Vector3


class Orbit(object, metaclass=ABCMeta):
    """
    An abstract class defining the orbit of a body
    """

    @abstractmethod
    def calculate(self, time):
        """
        Calculate current position of body with the current time and return it

        :param time: Delta Time
        :type time: float
        :return: position
        :rtype: :class:`euclid.Vector3`
        """

        pass

    def calculate_by_angle(self, angle):
        """
        Calculate current position of body with current angle in orbit and return it

        :param angle: current angle in orbit
        :type angle: float
        :return: position
        :rtype Vector3
        """

        pass

    def __str__(self):
        return "Orbit()"


class CircularOrbit(Orbit):
    """
    An Orbit subclass defining a circular orbit
    """

    def __init__(self, radius, orbital_period, inclination=0):
        """
        Creates a circular orbit with the given radius, orbital_period (siderial) and inclination

        :param radius: Radois of the orbit
        :type radius: float
        :param orbital_period: Duration of one orbit in seconds
        :type orbital_period: float
        :param inclination: Inclination of orbit in degrees
        :type: inclination: float
        """

        self.radius = radius
        self.orbital_period = orbital_period
        self.inclination = inclination

    def calculate(self, time):
        """
        Calculate current position of body with the current time and return it

        :param time: Delta Time
        :type time: float
        :return: position
        :rtype: :class:`euclid.Vector3`
        """

        return self.calculate_by_angle(360 * ((time % self.orbital_period) / self.orbital_period))

    def calculate_by_angle(self, angle):
        """
        Calculate current position of body with current angle in orbit and return it

        :param angle: current angle in orbit
        :type angle: float
        :return: position
        :rtype Vector3
        """

        angle = radians(angle)
        x = self.radius * cos(angle)
        y = self.radius * sin(angle)
        pos = Vector3(x, y, 0)
        if self.inclination != 0:
            pos = pos.rotate_around(Vector3(0, 1, 0), radians(self.inclination))
        return pos

    def __str__(self):
        return "CircualOrbit(radius=" + str(self.radius) + ")"

# orbit = EllipticOrbit(-1.4301960881, -11.26064, 114.20783, 149598023 / orbitmod / 10, 7.155, 365.256363 * dts)
# http://www.jgiesen.de/kepler/kepler.html
# class EllipticOrbit(Orbit):
#     def __init__(self, true_anomaly, longtitude_ascending_node, perihelion, semi_major_axis, inclination, orbital_period):
#         self.true_anomaly = true_anomaly
#         self.longtitude_ascending_node = longtitude_ascending_node
#         self.perihelion = perihelion
#         self.semi_major_axis = semi_major_axis
#         self.inclination = inclination
#         self.orbital_period = orbital_period
#
#         self.r = self.semi_major_axis * (1 - e ** 2) / (1 + e * cos(self.true_anomaly))
#
#     def calculate(self, time):
#         rot = 360 * ((time % self.orbital_period) / self.orbital_period)
#         return self.calculate_by_angle(rot)
#
#     def calculate_by_angle(self, rot):
#         rot = radians(rot)
#         x = self.r * (cos(self.longtitude_ascending_node) * cos(self.true_anomaly + self.perihelion) - sin(self.longtitude_ascending_node) * sin(self.true_anomaly + self.perihelion) * cos(self.inclination))
#         y = self.r * (sin(self.longtitude_ascending_node) * cos(self.true_anomaly + self.perihelion) + cos(self.longtitude_ascending_node) * sin(self.true_anomaly + self.perihelion) * cos(self.inclination))
#         z = self.r * sin(self.true_anomaly + self.perihelion) * sin(self.inclination)
#         return Vector3(x, y, z)
#
#     def __str__(self):
#         return "EllipticOrbit(true_anomaly=" + self.true_anomaly + ", longtitude_ascending_node=" + self.longtitude_ascending_node + ", perihelion=" + self.perihelion + ")"
