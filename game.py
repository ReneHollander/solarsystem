from math import floor

import pyglet
from euclid import *
from pyglet.gl import *
from pyglet.text import Label

from solarsystem.body import OrbitingBody, StationaryBody
from solarsystem.orbit import CircualOrbit
from util.camera import Camera, halfpi
from util.fpscounter import FPSCounter

pyglet.resource.path = ['resource/texture']

config = pyglet.gl.Config(sample_buffers=1, samples=8)
window = pyglet.window.Window(800, 600, config=config, caption='Solarsystem', resizable=True, vsync=False)
label_fpscounter = Label('', x=5, y=window.height - 5 - 12, font_size=12, bold=True, color=(127, 127, 127, 127))
fps_counter = FPSCounter(window, label_fpscounter)

label_timestep = Label('', x=10, y=10, font_size=18, bold=True, color=(127, 127, 127, 127))
hudelements = [label_fpscounter, label_timestep]

camera = Camera(window, position=Vector3(0, -400, 0), pitch=halfpi)
model_matrix = Matrix4()
proj_matrix = None
mvp = Matrix4()

timestep = 0
time = 0

orbitmod = 1000000.0
radiusmod = 1000.0
dts = 24 * 60 * 60
sun = StationaryBody(None, "sun", 12)
mercury = OrbitingBody(sun, "mercury", 4879 / radiusmod, CircualOrbit(57909050 / orbitmod, 87.969 * dts), 0.034, 58.646 * dts)
venus = OrbitingBody(sun, "venus", 6051 / radiusmod, CircualOrbit(108939000 / orbitmod, 224.701 * dts), 2.64, -243.025 * dts)
earth = OrbitingBody(sun, "earth", 6371 / radiusmod, CircualOrbit(149597500 / orbitmod, 365.256363 * dts), 23.4392811, 0.99726968 * dts)
moon = OrbitingBody(earth, "moon", 1737 / radiusmod, CircualOrbit(3840000 * 4 / orbitmod, 29.530589 * dts), 6.687, 27.321582 * dts)
mars = OrbitingBody(sun, "mars", 3398 / radiusmod, CircualOrbit(225000000 / orbitmod, 686.971 * dts), 25.19, 1.025957 * dts)
planets = [sun, mercury, venus, earth, moon, mars]


@window.event
def on_resize(width, height):
    global proj_matrix
    proj_matrix = Matrix4.new_perspective(45, float(width) / float(height), 0.1, 1000.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)

    label_fpscounter.y = window.height - 5 - 12

    return True


@window.event
def on_draw():
    window.clear()
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    for planet in planets:
        planet.render(mvp.__copy__())

    # ====== START HUD ======
    glMatrixMode(gl.GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(gl.GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window.width, 0, window.height, -1, 1)

    for hudelement in hudelements:
        hudelement.draw()

    glPopMatrix()
    glMatrixMode(gl.GL_MODELVIEW)
    glPopMatrix()
    # ====== STOP HUD ======


def update(dt):
    global time
    global mvp

    timestep = 60 * 60 * 24 * 7 * camera.time_multiplier
    time += dt * timestep
    label_timestep.text = "1 second = " + str(floor(timestep / 60 / 60)) + "hours"

    camera.update(dt)
    mvp = proj_matrix * camera.view_matrix * model_matrix

    for planet in planets:
        planet.update(time)


pyglet.clock.schedule(update)
pyglet.app.run()
