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

        self.view_matrix = Matrix4()
        self.orientation = Quaternion()
        self.position = Vector3()

    def update(self, delta):
        speed = 50
        speed *= delta / 1e1

        rotSpeed = 0.5 * speed

        dx = self.get_dx()
        dy = self.get_dy()

        if dy != 0:
            self.orientation = Quaternion.new_rotate_axis(-dy * rotSpeed, Vector3(1, 0, 0)) * self.orientation

        if dx != 0:
            self.orientation = Quaternion.new_rotate_axis(dx * rotSpeed, Vector3(0, 1, 0)) * self.orientation

        self.orientation.normalize()

        posDelta = Vector3()
        if self.mouse_locked:
            if self.keys[key.W]:
                posDelta.z += speed
            if self.keys[key.S]:
                posDelta.z -= speed
            if self.keys[key.A]:
                posDelta.x += speed
            if self.keys[key.D]:
                posDelta.x -= speed
            if self.keys[key.SPACE]:
                posDelta.y -= speed
            if self.keys[key.LCTRL]:
                posDelta.y += speed

        inverse = self.orientation.get_matrix().inverse().get_quaternion()
        self.position += inverse * posDelta

        matrix = self.orientation.get_matrix().translate(self.position.x, self.position.y, self.position.z)
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
