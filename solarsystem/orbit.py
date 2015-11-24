from math import sin, cos, radians, e

from abc import ABCMeta, abstractmethod
from euclid import Vector3


class Orbit(object, metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, time):
        pass

    def __str__(self):
        return "Orbit()"


class CircualOrbit(Orbit):
    def __init__(self, radius, orbital_period, inclination=0):
        self.radius = radius
        self.orbital_period = orbital_period
        self.inclination = inclination

    def calculate(self, time):
        rot = radians(360 * ((time % self.orbital_period) / self.orbital_period))
        x = self.radius * cos(rot)
        y = self.radius * sin(rot)
        pos = Vector3(x, y, 0)
        if self.inclination != 0:
            pos = pos.rotate_around(Vector3(0, 1, 0), radians(self.inclination))
        return pos

    def __str__(self):
        return "CircualOrbit(radius=" + self.radius + ")"


# orbit = EllipticOrbit(-1.4301960881, -11.26064, 114.20783, 149598023 / orbitmod / 10, 7.155, 365.256363 * dts)
# http://www.jgiesen.de/kepler/kepler.html
class EllipticOrbit(Orbit):
    def __init__(self, true_anomaly, longtitude_ascending_node, perihelion, semi_major_axis, inclination, orbital_period):
        self.true_anomaly = true_anomaly
        self.longtitude_ascending_node = longtitude_ascending_node
        self.perihelion = perihelion
        self.semi_major_axis = semi_major_axis
        self.inclination = inclination
        self.orbital_period = orbital_period

        self.r = self.semi_major_axis * (1 - e ** 2) / (1 + e * cos(self.true_anomaly))

    def calculate(self, time):
        rot = radians(360 * ((time % self.orbital_period) / self.orbital_period))
        x = self.r * (cos(self.longtitude_ascending_node) * cos(self.true_anomaly + self.perihelion) - sin(self.longtitude_ascending_node) * sin(self.true_anomaly + self.perihelion) * cos(self.inclination))
        y = self.r * (sin(self.longtitude_ascending_node) * cos(self.true_anomaly + self.perihelion) + cos(self.longtitude_ascending_node) * sin(self.true_anomaly + self.perihelion) * cos(self.inclination))
        z = self.r * sin(self.true_anomaly + self.perihelion) * sin(self.inclination)
        return Vector3(x, y, z)

    def __str__(self):
        return "EllipticOrbit(true_anomaly=" + self.true_anomaly + ", longtitude_ascending_node=" + self.longtitude_ascending_node + ", perihelion=" + self.perihelion + ")"
