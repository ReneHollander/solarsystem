from pyglet.gl import GLdouble


def toGlMatrix(matrix4):
    return (GLdouble * 16)(*matrix4)
