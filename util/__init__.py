"""
Created on 05.11.2015

:author: Rene Hollander 5BHIT

"""
import ctypes

import pyglet
from pyglet.text import decode_html

lightfv = ctypes.c_float * 4


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
