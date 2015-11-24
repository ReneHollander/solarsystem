import pyglet
from pyglet.text import decode_html


def load_string(filename):
    with pyglet.resource.file(filename) as file:
        string = file.read().decode("utf-8")
    return string


def load_html(filename):
    return decode_html(load_string(filename))
