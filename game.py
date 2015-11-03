from solarsystem.planet.earth import Earth
from pyrr import Quaternion, Matrix44, Vector3
import numpy as np
import ctypes
import math
import pyglet
from pyglet.gl import *
from pyglet.window import key

from util.camera import Camera

pyglet.resource.path = ['resource/mesh']

config = pyglet.gl.Config(sample_buffers=1, samples=8)
window = pyglet.window.Window(800, 600, config=config, caption='Demo', resizable=True, vsync=False)
fps_display = pyglet.window.FPSDisplay(window)

rotation = 0
earth = Earth()
lightfv = ctypes.c_float * 4
time = 0

orientation = Quaternion()
print(orientation)

keys = key.KeyStateHandler()
window.push_handlers(keys)
camera = Camera(keys)


def on_mouse_motion(x, y, dx, dy):
    camera.add_mouse_delta(dx, dy)


model_matrix = Matrix44.identity()
proj_matrix = None


@window.event
def on_resize(width, height):
    global proj_matrix
    proj_matrix = Matrix44.perspective_projection(math.radians(45), width / height, 0.1, 100.0)
    return True


@window.event
def on_draw():
    window.clear()

    print(proj_matrix)
    print(camera.view_matrix)
    print(model_matrix)

    mvp = proj_matrix * camera.view_matrix * model_matrix

    matrix = [
        mvp.m11, mvp.m12, mvp.m13, mvp.m14,
        mvp.m21, mvp.m22, mvp.m23, mvp.m24,
        mvp.m31, mvp.m32, mvp.m33, mvp.m34,
        mvp.m41, mvp.m42, mvp.m43, mvp.m44,
    ]

    matrix_gl = (GLdouble * len(matrix))(*matrix)

    glLoadMatrixd(matrix_gl)

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)

    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)

    glTranslated(0, .8, -20)
    earth.render()
    fps_display.draw()


def update(dt):
    global time
    time += dt * 60 * 60
    camera.update(dt)
    earth.update(time)


pyglet.clock.schedule(update)
pyglet.app.run()
