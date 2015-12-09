"""
Created on 09.12.2015

:author: Rene Hollander
"""

from util import auto_str


@auto_str
class Ray(object):
    """
    A ray with an origin and direction

    :var origin: Origin of the ray
    :type origin: :class:`euclid.Vector3`
    :var direction: Direction of the ray
    :type direction: :class:`euclid.Vector3`
    """

    def __init__(self, origin, direction):
        """
        Creates a new ray

        :param origin: Origin of the ray
        :type origin: :class:`euclid.Vector3`
        :param direction: Direction of the ray
        :type direction: :class:`euclid.Vector3`
        """

        self.origin = origin
        self.direction = direction
