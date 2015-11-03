import sys
from solarsystem.planet.earth import Earth
import ctypes
import pyglet
from pyglet.gl import *

pyglet.resource.path = ['resource/mesh']
window = pyglet.window.Window(800, 600, caption='Demo', resizable=True)

rotation = 0
earth = Earth()
lightfv = ctypes.c_float * 4
time = 0


@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    gluPerspective(40.0, float(width) / height, 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
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


def update(dt):
    global time
    time += dt * 60 * 60

    earth.update(time)


pyglet.clock.schedule(update)
pyglet.app.run()
