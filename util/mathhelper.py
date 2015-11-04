from pyrr import Vector3


def mulQuaternionVector3(quaternion, vector):
    quatVector = Vector3([quaternion.x, quaternion.y, quaternion.z])

    uv = quatVector.cross(vector)
    uuv = quatVector.cross(uv)

    uv *= (quaternion.w * 2)
    uuv *= 2

    return Vector3(vector) + uv + uuv
