from abc import ABCMeta, abstractmethod


class Orbit(object, metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, time):
        pass

    def __str__(self):
        return "Orbit()"


class CircualOrbit(Orbit):
    def __init__(self, radius):
        self.radius = radius

    def calculate(self, time):
        pass

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
