from pyrr import Quaternion, Matrix44, Vector3
import numpy as np
from pyglet.window import key
from pyrr.objects import matrix44

from util.mathhelper import mulQuaternionVector3


class Camera():
    def __init__(self, keys):
        self.keys = keys

        self.dx = 0
        self.dy = 0

        self.view_matrix = Matrix44.identity()
        self.orientation = Quaternion()
        self.position = Vector3()

    def update(self, delta):
        speed = 50
        speed *= delta / 1e1

        rotSpeed = 1.5 * speed

        dx = self.get_dx()
        dy = self.get_dy()

        if dy != 0:
            self.orientation = Quaternion.from_axis_rotation((-dy * rotSpeed, 1, 0), 0) * self.orientation

        if dx != 0:
            self.orientation = Quaternion.from_axis_rotation((dx * rotSpeed, 0, 1), 0) * self.orientation

        self.orientation.normalise()

        posDelta = Vector3()
        if self.keys[key.W]:
            posDelta.z += speed
        if self.keys[key.S]:
            posDelta.z -= speed
        if self.keys[key.A]:
            posDelta.x += speed
        if self.keys[key.D]:
            posDelta.x -= speed
        if self.keys[key.SPACE]:
            posDelta.y += speed
        if self.keys[key.LCTRL]:
            posDelta.y -= speed

        inverse = self.orientation.inverse
        self.position += mulQuaternionVector3(inverse, posDelta)

        matrix = self.orientation.matrix44 * Matrix44.from_translation(self.position)
        self.view_matrix = matrix

    def get_dx(self):
        tmp = self.dx
        self.dx = 0
        return tmp

    def get_dy(self):
        tmp = self.dy
        self.dy = 0
        return tmp

    def add_mouse_delta(self, dx, dy):
        self.dx += dx
        self.dy += dy
