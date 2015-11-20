from solarsystem.body import Planet
from solarsystem.orbit import Orbit, CircualOrbit


class Earth(Planet):
    def __init__(self):
        super(Earth, self).__init__(None, CircualOrbit(149598023), 6371, 23.4392811, 0.99726968 * 24 * 60 * 60)
