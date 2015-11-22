from math import sin, cos
from math import radians
from euclid import *
from pyglet.window import key, mouse, pyglet


class Camera():
    def __init__(self, window):
        self.window = window
        self.keys = key.KeyStateHandler()
        self.mouse_locked = False
        window.push_handlers(self.on_mouse_press, self.on_mouse_motion, self.on_key_press, self.on_key_release)

        self.dx = 0
        self.dy = 0

        self.yaw = 0.0
        self.pitch = 0.0
        self.position = Vector3()

        self.view_matrix = Matrix4()

    def update(self, delta):
        movementspeed = 30 * delta
        mousesensitivity = 0.01

        dx = self.get_dx()
        dy = self.get_dy()

        self.yaw += dx * mousesensitivity
        self.pitch -= dy * mousesensitivity

        if self.mouse_locked:
            if self.keys[key.W]:
                self.position.x -= movementspeed * sin(radians(self.yaw))
                self.position.z += movementspeed * cos(radians(self.yaw))
            if self.keys[key.S]:
                self.position.x += movementspeed * sin(radians(self.yaw))
                self.position.z -= movementspeed * cos(radians(self.yaw))
            if self.keys[key.A]:
                self.position.x -= movementspeed * sin(radians(self.yaw - 90))
                self.position.z += movementspeed * cos(radians(self.yaw - 90))
            if self.keys[key.D]:
                self.position.x -= movementspeed * sin(radians(self.yaw + 90))
                self.position.z += movementspeed * cos(radians(self.yaw + 90))
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
