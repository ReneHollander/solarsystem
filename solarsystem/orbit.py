"""
Created on 03.11.2015

:author: Rene Hollander
"""

from math import sin, cos, radians, sqrt, pi

from abc import ABCMeta, abstractmethod
from euclid import Vector3
from util import auto_str
from util.orbitalcalculations import gravitational_constant, eccentric_anomaly_from_mean, true_anomaly_from_eccentric


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
        :rtype: Vector3
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
        :rtype: Vector3
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


mass_sun = 1.9884 * 10 ** 30


# orbit = EllipticOrbit(-1.4301960881, -11.26064, 114.20783, 149598023 / orbitmod / 10, 7.155, 365.256363 * dts)
# http://www.jgiesen.de/kepler/kepler.html
@auto_str
class EllipticOrbit(Orbit):
    def __init__(self, apoapsis_radius, periapsis_radius, mass, longtitude_ascending_node, argument_of_periapsis, inclination):
        self.apoapsis_radius = apoapsis_radius
        self.periapsis_radius = periapsis_radius
        self.mass = mass
        self.longtitude_ascending_node = radians(longtitude_ascending_node)
        self.argument_of_periapsis = radians(argument_of_periapsis)
        self.inclination = radians(inclination)

        self.semi_major_axis = (self.apoapsis_radius + self.periapsis_radius) / 2.0
        self.eccentricity = (self.apoapsis_radius - self.periapsis_radius) / (self.apoapsis_radius + self.periapsis_radius)
        self.mu = gravitational_constant * (self.mass + mass_sun)
        self.orbital_period = 2.0 * pi * sqrt((self.semi_major_axis ** 3.0) / self.mu)
        self.mean_motion = 2.0 * pi / self.orbital_period

    def calculate(self, time):
        true_anomaly = true_anomaly_from_eccentric(self.eccentricity, eccentric_anomaly_from_mean(self.eccentricity, self.mean_motion * time))
        return self.calculate_by_angle(true_anomaly)

    def calculate_by_angle(self, rot):
        radius = self.semi_major_axis * (1.0 - self.eccentricity ** 2.0) / (1.0 + self.eccentricity * cos(rot))
        x = radius * (cos(self.longtitude_ascending_node) * cos(rot + self.periapsis_radius) - sin(self.longtitude_ascending_node) * sin(rot + self.periapsis_radius) * cos(self.inclination))
        y = radius * (sin(self.longtitude_ascending_node) * cos(rot + self.periapsis_radius) + cos(self.longtitude_ascending_node) * sin(rot + self.periapsis_radius) * cos(self.inclination))
        z = radius * sin(rot + self.periapsis_radius) * sin(self.inclination)
        return Vector3(x, y, z)


orbit = EllipticOrbit(152100000000, 147095000000, 5.97237 * 10 ** 24, -11.26064, 114.20783, 0.00005)
print(orbit)
pos = orbit.calculate(180 * 60 * 60 * 24)
print("x: " + str(pos.x / 1000) + ", y:" + str(pos.y / 1000) + ", z: " + str(pos.z / 1000))
