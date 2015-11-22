from abc import ABCMeta, abstractmethod
from math import sin, cos, radians

from euclid import Vector3


class Orbit(object, metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, time):
        pass

    def __str__(self):
        return "Orbit()"


class CircualOrbit(Orbit):
    def __init__(self, radius, orbital_period):
        self.radius = radius
        self.orbital_period = orbital_period

    def calculate(self, time):
        rot = radians(360 * ((time % self.orbital_period) / self.orbital_period))
        x = self.radius * cos(rot)
        y = self.radius * sin(rot)
        return Vector3(x=x, y=y)

    def __str__(self):
        return "CircualOrbit(radius=" + self.radius + ")"


class EllipticOrbit(Orbit):
    def __init__(self, true_anomaly, longtitude_ascending_node, perihelion):
        self.true_anomaly = true_anomaly
        self.longtitude_ascending_node = longtitude_ascending_node
        self.perihelion = perihelion

    def calculate(self, time):
        pass

    def __str__(self):
        return "EllipticOrbit(true_anomaly=" + self.true_anomaly + ", longtitude_ascending_node=" + self.longtitude_ascending_node + ", perihelion=" + self.perihelion + ")"
