"""
Created on 04.11.2015

:author: Rene Hollander
"""
from math import cos, sqrt, atan, tan
from math import sin

from pyglet.gl import GLdouble


def toGlMatrix(matrix4):
    """
    Converts the given matrix to be used by OpenGL

    :param matrix4: Matrix to convert
    :type matrix4: :class:`euclid.Matrix4`
    :return: Matrix to be used by OpenGL
    :rtype: No Idea
    """
    return (GLdouble * 16)(*matrix4)
