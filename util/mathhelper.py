from pyglet.gl import GLdouble


def toGlMatrix(matrix4):
    matrix_gl = (GLdouble * 16)(*matrix4)
    return matrix_gl
