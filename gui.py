import datetime
from math import floor

from pyglet_gui.buttons import pyglet
from pyglet_gui.constants import ANCHOR_TOP_LEFT, ANCHOR_BOTTOM_LEFT, ANCHOR_BOTTOM_RIGHT, ANCHOR_TOP_RIGHT, HALIGN_RIGHT
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.gui import Label
from pyglet_gui.manager import Manager
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.theme import Theme, ThemeFromPath
from util import load_string, halfpi
from util.bettergui import BetterOneTimeButton, BetterLabel
from util.fpscounter import FPSCounter
from util.orbitalcalculations import J2000

empty_theme = Theme({}, resources_path=None)


class GUI:
    def __init__(self, window, controls, bodies):
        self.window = window
        self.controls = controls
        self.bodies = bodies

        self.fps_counter = FPSCounter(window, self.fps_update)

        # Setup HUD elements
        self.label_fps = Label("", bold=True, font_name="Arial", font_size=12, color=(127, 127, 127, 127))
        self.label_time = Label("", bold=True, font_name="Arial", font_size=18, color=(127, 127, 127, 127))
        self.label_help = BetterLabel(load_string('help.txt'), bold=False, font_name="Arial", font_size=18, color=(170, 170, 170, 255), multiline=True, lblwidth=400)
        self.managers = [
            Manager(self.label_fps, window=window, theme=empty_theme, is_movable=False, anchor=ANCHOR_TOP_LEFT),
            Manager(self.label_time, window=window, theme=empty_theme, is_movable=False, anchor=ANCHOR_BOTTOM_LEFT)
        ]
        self.label_help_manager = Manager(self.label_help, window=window, theme=empty_theme, is_movable=False, anchor=ANCHOR_TOP_LEFT, offset=(0, -17))

        body_buttons = []
        for body in self.bodies:
            body_buttons.append(BodyButton(self, body).button)

        self.managers_when_not_locked = [
            Manager(VerticalContainer(body_buttons, align=HALIGN_RIGHT), window=window, theme=ThemeFromPath("theme/bodybutton"), is_movable=False, anchor=ANCHOR_TOP_RIGHT),
            Manager(HorizontalSlider(width=250), window=window, theme=ThemeFromPath("theme/timeslider"), is_movable=False, anchor=ANCHOR_BOTTOM_RIGHT)
        ]

    def fps_update(self, fps):
        self.label_fps.set_text(str(fps) + "fps")

    def update_time(self, timestep, solarsystem_time):
        self.label_time.set_text("1 second = " + str(floor(timestep / 60 / 60)) + "hours. Current Date: " + str(J2000 + datetime.timedelta(seconds=solarsystem_time)))

    def draw(self):
        if self.controls.draw_help_label:
            self.label_help_manager.draw()

        for manager in self.managers:
            manager.draw()

        if not self.controls.mouse_locked:
            for manager in self.managers_when_not_locked:
                manager.draw()


class BodyButton:
    def __init__(self, gui, body):
        self.gui = gui
        self.body = body
        self.batch = pyglet.graphics.Batch()
        self.button = BetterOneTimeButton(body.name, on_release=self.state_change, color=(body.color["r"], body.color["g"], body.color["b"], 255))

    def state_change(self, state):
        self.gui.controls.camera.position = self.body.xyz + [0, 50, 0]
        self.gui.controls.camera._pitch = -halfpi
