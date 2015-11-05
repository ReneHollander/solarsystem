import math
from abc import ABCMeta

from euclid import Vector3
from pywavefront import Wavefront

from util import read_resource_to_string
from util.shader import Shader


class Planet(object, metaclass=ABCMeta):
    def __init__(self, orbit, mean_radius, axial_tilt, sidereal_rotation_period):
        self.name = self.__class__.__name__
        self.orbit = orbit
        self.mean_radius = mean_radius
        self.axial_tilt = axial_tilt
        self.sidereal_rotation_period = sidereal_rotation_period

        self.obj = Wavefront(self.name.lower() + ".obj")
        self.shader = Shader(read_resource_to_string('base.vert'), read_resource_to_string('base.frag'))
        self.shader.link()
        self.shader.enumerate_uniforms()

    def update(self, time):
        self.timefactor = (time % self.sidereal_rotation_period) / self.sidereal_rotation_period

    def render(self, mvp):
        matrix = mvp.__copy__()
        matrix.translate(0, .8, -20)
        matrix.rotate_axis(math.radians(-90 - self.axial_tilt), Vector3(0, 0, 1))
        matrix.rotate_axis(math.radians(-360 * self.timefactor), Vector3(1, 0, 0))
        matrix.rotate_axis(math.radians(90), Vector3(0, 0, 1))
        matrix.rotate_axis(math.radians(0), Vector3(0, 1, 0))
        # glLoadMatrixd(toGlMatrix(matrix))
        self.shader.bind()
        self.shader.uniform_matrixd("transformation", matrix)
        self.obj.draw()
        self.shader.unbind()

    def __str__(self):
        return self.name + "({orbit: " + str(self.orbit) + ", mean_radius: \"" + str(
            self.mean_radius) + "\", axial_tilt: \"" + str(self.axial_tilt) + "\", sidereal_rotation_period: \"" + str(
            self.sidereal_rotation_period) + "\"obj: \"" + str(self.obj) + "\"})"
