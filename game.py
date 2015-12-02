"""
Created on 04.11.2015

:author: Rene Hollander, Paul Kalauner
"""

from math import floor

import pyglet
from euclid import *
from pyglet.gl import *
from pyglet.text import Label
from solarsystem.loader import load_bodies
from util import load_string, toGlMatrix
from util.camera import Camera, halfpi
from util.fpscounter import FPSCounter
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

fullscreen = False
draw_skybox = True

# looad the bodies from the json files
planets = load_bodies("bodies")


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


def toggle_fullscreen(override):
    global fullscreen
    if override is not None:
        fullscreen = override
    else:
        fullscreen = not fullscreen
    window.set_fullscreen(fullscreen)


# Create a new camera
camera = Camera(window, position=Vector3(0, -420, 0), pitch=halfpi, callbacks={'toggle_draw_orbits': toggle_draw_orbits,
                                                                               'toggle_draw_textures': toggle_draw_textures,
                                                                               'toggle_fullscreen': toggle_fullscreen})
# Create model and projection matrices
model_matrix = Matrix4()
proj_matrix = None
mvp = Matrix4()

# time
timestep = 0
solarsystem_time = 0
time = solarsystem_time

# create the skyshpere
skybox = SkySphere("milkyway.jpg", 5500)


# list of all bodies to be drawn


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
        skybox_matrix.translate(-camera.position.x, -camera.position.y, -camera.position.z)
        skybox_matrix.rotate_axis(math.radians(-90), Vector3(1, 0, 0))
        glLoadMatrixd(toGlMatrix(skybox_matrix))
        skybox.draw()

    # reemable opengl flags
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)

    # loop through bodies and draw
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

    # update every bodies
    for planet in planets:
        planet.update(solarsystem_time)


# starts the application
pyglet.clock.schedule(update)
pyglet.app.run()
