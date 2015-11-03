from abc import ABCMeta, abstractmethod

from pywavefront import Wavefront


class Planet(object, metaclass=ABCMeta):
    def __init__(self, orbit, mean_radius, axial_tilt, sidereal_rotation_period):
        self.name = self.__class__.__name__
        self.orbit = orbit
        self.mean_radius = mean_radius
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period

        self.obj = Wavefront(self.name.lower() + ".obj")

    def render(self):
        self.obj.draw()

    def __str__(self):
        return self.name + "({" \
                           "orbit: " + str(self.orbit) + ", " \
                                                         "mean_radius: \"" + str(self.mean_radius) + "\", " \
                                                                                                     "axial_tilt: \"" + str(
            self.axial_tilt) + "\", " \
                               "sidereal_rotation_period: \"" + str(self.sidereal_rotation_period) + "\"" \
                                                                                                     "obj: \"" + str(
            self.obj) + "\"" \
                        "})"
