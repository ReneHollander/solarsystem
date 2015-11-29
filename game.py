from math import floor

import pyglet
from euclid import *
from pyglet.gl import *
from pyglet.text import Label
from solarsystem.body import OrbitingBody, StationaryBody
from solarsystem.orbit import CircularOrbit
from util import load_string
from util.camera import Camera, halfpi
from util.fpscounter import FPSCounter
from util.mathhelper import toGlMatrix
from util.skybox import SkySphere

# Register resource locations in pyglet resource loader
pyglet.resource.path = ['resource/texture', 'resource/text']
pyglet.resource.reindex()

# Configure and setup window
config = pyglet.gl.Config(sample_buffers=1, samples=8, depth_size=24)
window = pyglet.window.Window(800, 600, config=config, caption='Solarsystem', resizable=True, vsync=False)

# Setup HUD elements
label_fpscounter = Label('', x=5, y=window.height - 5 - 12, font_size=12, bold=True, color=(127, 127, 127, 127))
fps_counter = FPSCounter(window, label_fpscounter)
label_timestep = Label('', x=10, y=10, font_size=18, bold=True, color=(127, 127, 127, 127))
help_label = Label(load_string('help.txt'), font_size=16, x=5, y=window.height - 5 - 12 - 2 - 16, color=(170, 170, 170, 255), width=400, multiline=True)
hudelements = [label_fpscounter, label_timestep]

draw_skybox = True


def toggle_draw_orbits():
    """
    Toggles the plotting of the orbits
    """
    for cur in planets:
        cur.draw_orbit = not cur.draw_orbit


def toggle_draw_textures():
    """
    Toggles the drawing of the textures
    """
    global draw_skybox
    draw_skybox = not draw_skybox
    for cur in planets:
        cur.draw_texture = not cur.draw_texture


# Create a new camera
camera = Camera(window, position=Vector3(0, -420, 0), pitch=halfpi, callbacks={'toggle_draw_orbits': toggle_draw_orbits,
                                                                               'toggle_draw_textures': toggle_draw_textures})
# Create model and projection matrices
model_matrix = Matrix4()
proj_matrix = None
mvp = Matrix4()

# time
timestep = 0
solarsystem_time = 0
time = solarsystem_time

# values to normalize orbital elements
orbitmod = 1000000.0
radiusmod = 1000.0
dts = 24 * 60 * 60

# create the skyshpere
skybox = SkySphere("milkyway.jpg", 5500)

# create all planets with their specifig orbital elements
sun = StationaryBody(None, "sun", {"r": 250, "g": 150, "b": 26}, 12, 7.25, 25.83 * dts)
mercury = OrbitingBody(sun, "mercury", {"r": 159, "g": 141, "b": 127}, 4879 / radiusmod, CircularOrbit(57909050 / orbitmod, 87.969 * dts, 3.38), 0.034, 58.646 * dts)
venus = OrbitingBody(sun, "venus", {"r": 146, "g": 71, "b": 14}, 6051 / radiusmod, CircularOrbit(108939000 / orbitmod, 224.701 * dts, 3.86), 2.64, -243.025 * dts)
earth = OrbitingBody(sun, "earth", {"r": 29, "g": 60, "b": 109}, 6371 / radiusmod, CircularOrbit(149597500 / orbitmod, 365.256363 * dts, 7.155), 23.4392811, 0.99726968 * dts)
moon = OrbitingBody(earth, "moon", {"r": 118, "g": 118, "b": 118}, 1737 / radiusmod, CircularOrbit(3840000 * 4 / orbitmod, 29.530589 * dts, 5.145), 6.687, 27.321582 * dts)
mars = OrbitingBody(sun, "mars", {"r": 114, "g": 90, "b": 66}, 3398 / radiusmod, CircularOrbit(225000000 / orbitmod, 686.971 * dts, 5.65), 25.19, 1.025957 * dts)
ceres = OrbitingBody(sun, "ceres", {"r": 182, "g": 165, "b": 149}, 473 / radiusmod * 3, CircularOrbit(414015000 / orbitmod / 1.3, 1681.63 * dts, 9.20), 4, 0.3781 * dts)
jupiter = OrbitingBody(sun, "jupiter", {"r": 192, "g": 161, "b": 133}, 66854 / radiusmod / 5, CircularOrbit(778547200 / orbitmod / 2, 4332.59 * dts, 6.09), 3.13, 0.4135 * dts)
saturn = OrbitingBody(sun, "saturn", {"r": 215, "g": 191, "b": 147}, 58232 / radiusmod / 5, CircularOrbit(1433449369 / orbitmod / 2, 10759.22 * dts, 5.51), 26.73, 0.4395 * dts)
uranus = OrbitingBody(sun, "uranus", {"r": 160, "g": 209, "b": 216}, 25362 / radiusmod / 2, CircularOrbit(2875 / 2, 30688 * dts, 6.48), 97.77, 0.71833 * dts)
neptune = OrbitingBody(sun, "neptune", {"r": 61, "g": 108, "b": 200}, 24622 / radiusmod / 2, CircularOrbit(4498542650 / orbitmod / 2, 60190 * dts, 6.43), 28.32, 0.6713 * dts)
pluto = OrbitingBody(sun, "pluto", {"r": 174, "g": 131, "b": 97}, 1187 / radiusmod * 3, CircularOrbit(5907 / 2, 90581 * dts, 11.88), 119.591, 6.387230 * dts)
makemake = OrbitingBody(sun, "makemake", {"r": 137, "g": 81, "b": 68}, 715 / radiusmod * 3, CircularOrbit(6857 / 2, 112897 * dts, 29.00685), 0, 0.3237 * dts)
eris = OrbitingBody(sun, "eris", {"r": 162, "g": 180, "b": 190}, 1163 / radiusmod * 3, CircularOrbit(10167 / 2, 203830 * dts, 44.0445), 0, 1.0791 * dts)
# list of all planets to be drawn
planets = [sun, mercury, venus, earth, moon, mars, ceres, jupiter, saturn, uranus, neptune, pluto, makemake, eris]


@window.event
def on_resize(width, height):
    """
    Capture pyglet resize event

    :param width: New width
    :param height: New height
    """

    global proj_matrix
    # recalculate projection matrix
    proj_matrix = Matrix4.new_perspective(45, float(width) / float(height), 0.1, 16000.0)
    # set new viewport
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)

    # update label positions
    label_fpscounter.y = window.height - 5 - 12
    help_label.y = window.height - 5 - 12 - 2 - 16

    return True


@window.event
def on_draw():
    """
    Redraw the screen
    """

    # reset window and set all needed opengl flags
    window.clear()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    # draw skybox if requested
    if draw_skybox:
        skybox_matrix = mvp.__copy__()
        print(camera.position)
        skybox_matrix.translate(-camera.position.x, -camera.position.y, -camera.position.z)
        skybox_matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        glLoadMatrixd(toGlMatrix(skybox_matrix))
        skybox.draw()

    # reemable opengl flags
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)

    # loop through planets and draw
    for planet in planets:
        planet.draw(mvp.__copy__())

    # ====== START HUD ======
    # create an orthographic projection (2d)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window.width, 0, window.height, -1, 1)

    # draw all hudelements
    for hudelement in hudelements:
        hudelement.draw()

    if camera.draw_help_label:
        help_label.draw()

    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    # ====== STOP HUD ======


def update(dt):
    """
    Update time, Recalculate orbital positions

    :param dt: Time since last update
    """
    global solarsystem_time
    global mvp
    global time

    # recalculate solarsystem time
    timestep = 60 * 60 * 24 * 7 * camera.time_multiplier
    solarsystem_time += dt * timestep
    time += dt
    label_timestep.text = "1 second = " + str(floor(timestep / 60 / 60)) + "hours"

    if not camera.toggled_help_label and time >= 10:
        camera.draw_help_label = False

    # update the camera
    camera.update(dt)
    # recalculate mvp matrix
    mvp = proj_matrix * camera.view_matrix * model_matrix

    # update every planet
    for planet in planets:
        planet.update(solarsystem_time)


# starts the application
pyglet.clock.schedule(update)
pyglet.app.run()
