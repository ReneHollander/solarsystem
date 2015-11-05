import ctypes

import pyglet
from euclid import *
from pyglet.gl import *
from pyglet.window import key

from solarsystem.planet.earth import Earth
from util.camera import Camera

pyglet.resource.path = ['resource/mesh']

config = pyglet.gl.Config(sample_buffers=1, samples=8)
window = pyglet.window.Window(800, 600, config=config, caption='Solarsystem', resizable=True, vsync=False)
fps_display = pyglet.window.FPSDisplay(window)
rotation = 0
earth = Earth()
lightfv = ctypes.c_float * 4
time = 0
orientation = Quaternion()
camera = Camera(window)
model_matrix = Matrix4()
proj_matrix = None
mvp = Matrix4()

# 5BHIT ist beste Klasse!

# Window resize event
@window.event
def on_resize(width, height):
    global proj_matrix
    proj_matrix = Matrix4.new_perspective(45, float(width) / float(height), 0.1, 100.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    return True


# Called if window requests to render
@window.event
def on_draw():
    window.clear()
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    earth.render(mvp)
    fps_display.draw()

# Updte time and recalculate mvp
def update(dt):
    global time
    time += dt * 60 * 60
    camera.update(dt)
    global mvp
    mvp = proj_matrix * camera.view_matrix * model_matrix
    earth.update(time)


pyglet.clock.schedule(update)
pyglet.app.run()
