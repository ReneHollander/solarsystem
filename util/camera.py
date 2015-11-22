from math import sin, cos, pi

from euclid import *
from pyglet.window import key, mouse, pyglet

halfpi = pi / 2.0


class Camera():
    def __init__(self, window, position=Vector3(), yaw=0.0, pitch=0.0):
        self.window = window
        self.keys = key.KeyStateHandler()
        self.mouse_locked = False
        self.dx = 0
        self.dy = 0
        self.yaw = yaw
        self.pitch = pitch
        self.position = position
        self.view_matrix = Matrix4()
        self.time_multiplier = 1.0
        self.time_multiplier_before_pause = 1.0

        window.push_handlers(self.on_mouse_press, self.on_mouse_motion, self.on_key_press, self.on_key_release)

    def update(self, delta):
        movementspeed = 30 * delta
        mousesensitivity = 0.01

        dx = self.get_dx()
        dy = self.get_dy()

        self.yaw += dx * mousesensitivity
        self.pitch -= dy * mousesensitivity

        if self.pitch > halfpi:
            self.pitch = halfpi
        if self.pitch < -halfpi:
            self.pitch = -halfpi

        if self.mouse_locked:
            if self.keys[key.LSHIFT]:
                movementspeed *= 10
            if self.keys[key.W]:
                self.position.x -= movementspeed * sin(self.yaw)
                self.position.z += movementspeed * cos(self.yaw)
            if self.keys[key.S]:
                self.position.x += movementspeed * sin(self.yaw)
                self.position.z -= movementspeed * cos(self.yaw)
            if self.keys[key.A]:
                self.position.x -= movementspeed * sin(self.yaw - 90)
                self.position.z += movementspeed * cos(self.yaw - 90)
            if self.keys[key.D]:
                self.position.x -= movementspeed * sin(self.yaw + 90)
                self.position.z += movementspeed * cos(self.yaw + 90)
            if self.keys[key.SPACE]:
                self.position.y -= movementspeed
            if self.keys[key.LCTRL]:
                self.position.y += movementspeed

        matrix = Matrix4()
        matrix.rotate_axis(self.pitch, Vector3(1, 0, 0))
        matrix.rotate_axis(self.yaw, Vector3(0, 1, 0))
        matrix.translate(self.position.x, self.position.y, self.position.z)

        self.view_matrix = matrix

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True
        if symbol == key.ESCAPE:
            self.window.set_exclusive_mouse(False)
            self.mouse_locked = False
            return pyglet.event.EVENT_HANDLED
        # Key code 43: Plus key
        if symbol == key.NUM_ADD or symbol == 43:
            self.time_multiplier += 0.1
        # Key code 45: Minus key
        if symbol == key.NUM_SUBTRACT or symbol == 45:
            self.time_multiplier -= 0.1
        if symbol == key.P:
            if self.time_multiplier == 0:
                self.time_multiplier = self.time_multiplier_before_pause
            else:
                self.time_multiplier_before_pause = self.time_multiplier
                self.time_multiplier = 0

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.window.set_exclusive_mouse(True)
            self.mouse_locked = True

    def get_dx(self):
        tmp = self.dx
        self.dx = 0
        return tmp

    def get_dy(self):
        tmp = self.dy
        self.dy = 0
        return tmp

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_locked:
            self.dx += dx
            self.dy += dy
