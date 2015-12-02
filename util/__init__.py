"""
Created on 05.11.2015

:author: Rene Hollander 5BHIT

"""
import ctypes
import time as time_

import pyglet
from pyglet.text import decode_html

lightfv = ctypes.c_float * 4
dts = 24 * 60 * 60


def load_string(filename):
    """
    loads the given file
    :param filename: name of the file that should be loaded
    :return: content of the file
    """
    with pyglet.resource.file(filename) as file:
        string = file.read().decode("utf-8")
    return string


def load_html(filename):
    """
    Loads a HTML-file
    :param filename: name of the file that should be loaded
    :return: content of the file
    """
    return decode_html(load_string(filename))


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


def millis():
    return int(round(time_.time() * 1000))
