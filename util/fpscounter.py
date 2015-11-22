from math import floor
from time import time


class FPSCounter(object):
    update_period = 0.25

    def __init__(self, window, label=None):
        self.window = window
        self.label = label
        self._window_flip = window.flip
        window.flip = self._hook_flip

        self.time = 0.0
        self.last_time = time()
        self.count = 0
        self.fps = 0

    def update(self):
        from time import time
        t = time()
        self.count += 1
        self.time += t - self.last_time
        self.last_time = t

        if self.time >= self.update_period:
            self.set_fps(self.count / self.update_period)
            self.time %= self.update_period
            self.count = 0

    def set_fps(self, fps):
        self.fps = fps
        if self.label:
            self.label.text = str(floor(self.fps)) + "fps"

    def _hook_flip(self):
        self.update()
        self._window_flip()
