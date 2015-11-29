from math import floor
import pyglet
from euclid import *
from pyglet.gl import *
from pyglet.text import Label, HTMLLabel

from solarsystem.body import OrbitingBody, StationaryBody
from solarsystem.orbit import CircualOrbit
from util import load_string
from util.camera import Camera, halfpi
from util.fpscounter import FPSCounter

pyglet.resource.path = ['resource/texture', 'resource/text']
pyglet.resource.reindex()

config = pyglet.gl.Config(sample_buffers=1, samples=8, depth_size=24)
window = pyglet.window.Window(800, 600, config=config, caption='Solarsystem', resizable=True, vsync=False)

label_fpscounter = Label('', x=5, y=window.height - 5 - 12, font_size=12, bold=True, color=(127, 127, 127, 127))
fps_counter = FPSCounter(window, label_fpscounter)

label_timestep = Label('', x=10, y=10, font_size=18, bold=True, color=(127, 127, 127, 127))
help_label = HTMLLabel(load_string('help.html'), x=5, y=window.height - 5 - 12 - 2 - 16, width=300, multiline=True)

hudelements = [label_fpscounter, label_timestep]


def toggle_draw_orbits():
    for cur in planets:
        cur.draw_orbit = not cur.draw_orbit


def toggle_draw_textures():
    for cur in planets:
        cur.draw_texture = not cur.draw_texture

camera = Camera(window, position=Vector3(0, -420, 0), pitch=halfpi, callbacks={'toggle_draw_orbits': toggle_draw_orbits,
                                                                               'toggle_draw_textures': toggle_draw_textures})
model_matrix = Matrix4()
proj_matrix = None
mvp = Matrix4()

timestep = 0
solarsystem_time = 0
time = solarsystem_time

orbitmod = 1000000.0
radiusmod = 1000.0
dts = 24 * 60 * 60

sun = StationaryBody(None, "sun", 12, 7.25, 25.83 * dts)
mercury = OrbitingBody(sun, "mercury", 4879 / radiusmod, CircualOrbit(57909050 / orbitmod, 87.969 * dts, 3.38), 0.034, 58.646 * dts)
venus = OrbitingBody(sun, "venus", 6051 / radiusmod, CircualOrbit(108939000 / orbitmod, 224.701 * dts, 3.86), 2.64, -243.025 * dts)
earth = OrbitingBody(sun, "earth", 6371 / radiusmod, CircualOrbit(149597500 / orbitmod, 365.256363 * dts, 7.155), 23.4392811, 0.99726968 * dts)
moon = OrbitingBody(earth, "moon", 1737 / radiusmod, CircualOrbit(3840000 * 4 / orbitmod, 29.530589 * dts, 5.145), 6.687, 27.321582 * dts)
mars = OrbitingBody(sun, "mars", 3398 / radiusmod, CircualOrbit(225000000 / orbitmod, 686.971 * dts, 5.65), 25.19, 1.025957 * dts)
planets = [sun, mercury, venus, earth, moon, mars]


@window.event
def on_resize(width, height):
    global proj_matrix
    proj_matrix = Matrix4.new_perspective(45, float(width) / float(height), 0.1, 1000.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)

    label_fpscounter.y = window.height - 5 - 12
    help_label.y = window.height - 5 - 12 - 2 - 16

    return True


@window.event
def on_draw():
    window.clear()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glShadeModel(GL_SMOOTH)

    for planet in planets:
        planet.render(mvp.__copy__())

    # ====== START HUD ======
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window.width, 0, window.height, -1, 1)

    for hudelement in hudelements:
        hudelement.draw()

    if camera.draw_help_label:
        help_label.draw()

    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    # ====== STOP HUD ======


def update(dt):
    global solarsystem_time
    global mvp
    global time

    timestep = 60 * 60 * 24 * 7 * camera.time_multiplier
    solarsystem_time += dt * timestep
    time += dt
    label_timestep.text = "1 second = " + str(floor(timestep / 60 / 60)) + "hours"

    if not camera.toggled_help_label and time >= 5:
        camera.toggled_help_label = False
        camera.draw_help_label = False

    camera.update(dt)
    mvp = proj_matrix * camera.view_matrix * model_matrix

    for planet in planets:
        planet.update(solarsystem_time)
pyglet.clock.schedule(update)
pyglet.app.run()
