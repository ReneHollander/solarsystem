import ctypes
import pyglet
from euclid import *
from pyglet.gl import *
from solarsystem.body import Planet
from solarsystem.orbit import CircualOrbit
from util.camera import Camera

pyglet.resource.path = ['resource/texture']

config = pyglet.gl.Config(sample_buffers=1, samples=8)
window = pyglet.window.Window(800, 600, config=config, caption='Solarsystem', resizable=True, vsync=False)
fps_display = pyglet.window.FPSDisplay(window)
rotation = 0
lightfv = ctypes.c_float * 4
time = 0
orientation = Quaternion()
camera = Camera(window)
model_matrix = Matrix4()
proj_matrix = None
mvp = Matrix4()

orbitmod = 1000000.0
radiusmod = 1000.0

print(149597500 / orbitmod)

earth = Planet(None, "earth", CircualOrbit(149597500 / orbitmod, 365.256363 * 24 * 60 * 60), 6371 / radiusmod,
               23.4392811,
               0.99726968 * 24 * 60 * 60)
moon = Planet(earth, "moon", CircualOrbit(384000 / orbitmod, 29.530589 * 24 * 60 * 60), 1737 / radiusmod, 6.687,
              27.321582 * 24 * 60 * 60)

planets = [earth, moon]


@window.event
def on_resize(width, height):
    global proj_matrix
    proj_matrix = Matrix4.new_perspective(45, float(width) / float(height), 0.1, 100.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    # glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    # glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    # glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    for planet in planets:
        planet.render(mvp.__copy__())

    # earth.render(mvp.__copy__())
    # mvp.translate(40, 0, 0)
    # moon.render(mvp.__copy__())

    fps_display.draw()


def update(dt):
    global time
    time += dt * 60 * 60 * 24 * 7
    camera.update(dt)
    global mvp
    mvp = proj_matrix * camera.view_matrix * model_matrix
    for planet in planets:
        planet.update(time)


pyglet.clock.schedule(update)
pyglet.app.run()
