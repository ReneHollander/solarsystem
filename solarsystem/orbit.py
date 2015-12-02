"""
Created on 03.11.2015

:author: Rene Hollander
"""

from math import sin, cos, radians, sqrt, pi, fmod

from abc import ABCMeta, abstractmethod
from euclid import Vector3
from util import auto_str
from util.orbitalcalculations import gravitational_constant, eccentric_anomaly_from_mean, true_anomaly_from_eccentric


@auto_str
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

        :param angle: current angle in orbit in radians
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
        :param inclination: Inclination of orbit in radians
        :type: inclination: float
        """

        self.radius = radius
        self.orbital_period = orbital_period
        self.inclination = inclination

    def calculate(self, time):
        return self.calculate_by_angle(radians(360 * ((time % self.orbital_period) / self.orbital_period)))

    def calculate_by_angle(self, angle):
        angle = fmod(angle, 2.0 * pi)
        x = self.radius * cos(angle)
        y = self.radius * sin(angle)
        pos = Vector3(x, y, 0)
        if self.inclination != 0:
            pos = pos.rotate_around(Vector3(0, 1, 0), self.inclination)
        return pos


mass_sun = 1.9884 * 10 ** 30


class EllipticOrbit(Orbit):
    """
    An elliptical orbit calculated from orbital elements

    Sources:
    http://astronomy.stackexchange.com/questions/12716/simulate-an-orbit-with-orbital-elements
    http://www.orbiter-forum.com/showthread.php?t=26682
    https://downloads.rene-schwarz.com/download/M001-Keplerian_Orbit_Elements_to_Cartesian_State_Vectors.pdf
    https://www.physicsforums.com/threads/calculating-elliptic-orbits-in-cartesian-coordinates.712979/

    :var semi_major_axis: Semi-mahor axis calculated from the provided apoapsis and periapsis
    :type semi_major_axis: float
    :var eccentricity: Eccentricity calculated from the provided apoapsis and periapsis
    :type eccentricity: float
    :var orbital_period: Orbital period calculated from the semi-major axis and mass in seconds
    :type orbital_period: float
    :var mean_motion: Mean motion in radians per second
    :type mean_motion: float
    """

    def __init__(self, apoapsis, periapsis, mass, longtitude_ascending_node, argument_of_periapsis, inclination):
        """
        Creates a new elliptical orbit from the given parameters

        :param apoapsis: Apoapsis in meters
        :type apoapsis: float
        :param periapsis: Periapsis in meters
        :type periapsis: float
        :param mass: Mass of the body in kilograms
        :type mass: float
        :param longtitude_ascending_node: Longtitude of the ascending node in radians
        :type longtitude_ascending_node: float
        :param argument_of_periapsis: Argument of the periapsis in radians
        :type argument_of_periapsis: float
        :param inclination: Inclination of the orbit in radians
        :type inclination: float
        """

        self.apoapsis = apoapsis
        self.periapsis = periapsis
        self.mass = mass
        self.longtitude_ascending_node = longtitude_ascending_node
        self.argument_of_periapsis = argument_of_periapsis
        self.inclination = inclination

        self.semi_major_axis = (self.apoapsis + self.periapsis) / 2.0
        self.eccentricity = (self.apoapsis - self.periapsis) / (self.apoapsis + self.periapsis)
        self.orbital_period = 2.0 * pi * sqrt((self.semi_major_axis ** 3.0) / gravitational_constant * (self.mass + mass_sun))
        self.mean_motion = 2.0 * pi / self.orbital_period

    def calculate(self, time):
        true_anomaly = true_anomaly_from_eccentric(self.eccentricity, eccentric_anomaly_from_mean(self.eccentricity, self.mean_motion * time))
        return self.calculate_by_angle(true_anomaly)

    def calculate_by_angle(self, angle):
        angle = fmod(angle, 2.0 * pi)
        radius = self.semi_major_axis * (1.0 - self.eccentricity ** 2.0) / (1.0 + self.eccentricity * cos(angle))
        x = radius * (cos(self.longtitude_ascending_node) * cos(angle + self.periapsis) - sin(self.longtitude_ascending_node) * sin(angle + self.periapsis) * cos(self.inclination))
        y = radius * (sin(self.longtitude_ascending_node) * cos(angle + self.periapsis) + cos(self.longtitude_ascending_node) * sin(angle + self.periapsis) * cos(self.inclination))
        z = radius * sin(angle + self.periapsis) * sin(self.inclination)
        return Vector3(x, y, z)


orbit = EllipticOrbit(152100000000, 147095000000, 5.97237 * 10 ** 24, radians(-11.26064), radians(114.20783), radians(0.00005))
print(orbit)
print("orbital period: " + str(orbit.orbital_period / 60 / 60 / 24))
for day in range(0, 360):
    pos = orbit.calculate_by_angle(radians(day))
    print("x: " + str(pos.x / 1000000000) + ", y:" + str(pos.y / 1000000000) + ", z: " + str(pos.z / 1000000000))

    # TODO convert angles in json files to radians
    # TODO add parent body to orbit
    # TODO add support for elliptical orbits to the json loader
    # TODO convert all orbits to use the new elliptical calculations
