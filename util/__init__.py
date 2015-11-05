import pyglet


def read_resource_to_string(name):
    return pyglet.resource.file(name).readlines()
