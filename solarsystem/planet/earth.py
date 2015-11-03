from solarsystem.body import Planet
from solarsystem.util import Orbit


class Earth(Planet):
    def __init__(self):
        super(Earth, self).__init__(
            Orbit(
                152100000,
                147095000,
                149598023,
                0.0167086,
                365.256363004,
                29.78,
                358.617,
                7.155,
                1.57869
            ), 6371, 23.4392811, 0.99726968)
