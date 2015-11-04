from pyglet.gl import GLdouble
from pyrr import Vector3


def mulQuaternionVector3(quaternion, vector):
    quatVector = Vector3([quaternion.x, quaternion.y, quaternion.z])

    uv = quatVector.cross(vector)
    uuv = quatVector.cross(uv)

    uv *= (quaternion.w * 2)
    uuv *= 2

    return Vector3(vector) + uv + uuv


def toGlMatrix(matrix44):
    matrix = [
        matrix44.m11, matrix44.m12, matrix44.m13, matrix44.m14,
        matrix44.m21, matrix44.m22, matrix44.m23, matrix44.m24,
        matrix44.m31, matrix44.m32, matrix44.m33, matrix44.m34,
        matrix44.m41, matrix44.m42, matrix44.m43, matrix44.m44,
    ]

    matrix_gl = (GLdouble * len(matrix))(*matrix)
    return matrix_gl
