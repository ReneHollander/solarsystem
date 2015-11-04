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
    proj_matrix = Matrix44.perspective_projection(45, float(width) / float(height), 0.1, 100.0)
    print(proj_matrix)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    # gluPerspective(40.0, float(width) / height, 1, 100.0)
    # glEnable(GL_DEPTH_TEST)
    # glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()

    mvp = proj_matrix * camera.view_matrix * model_matrix

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glTranslated(0, .8, -20)
    earth.render(mvp)
    fps_display.draw()


def update(dt):
    global time
    time += dt * 60 * 60
    camera.update(dt)
    earth.update(time)


pyglet.clock.schedule(update)
pyglet.app.run()
