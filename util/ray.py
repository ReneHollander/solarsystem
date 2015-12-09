from util import auto_str


@auto_str
class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
