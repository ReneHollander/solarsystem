from solarsystem.body import Planet
from solarsystem.orbit import Orbit, CircualOrbit


class Moon(Planet):
    def __init__(self):
        super(Moon, self).__init__(None, CircualOrbit(149598023), 6371, 23.4392811, 0.99726968 * 24 * 60 * 60)
