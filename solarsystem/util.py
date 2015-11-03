class Orbit:
    def __init__(self,
                 aphelion,
                 perihelion,
                 semi_major_axis,
                 eccentricity,
                 orbital_period,
                 average_orbital_speed,
                 mean_anomaly,
                 inclination_to_sun,
                 inclination_to_invariable_plane
                 ):
        self.aphelion = aphelion
        self.perihelion = perihelion
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.orbital_period = orbital_period
        self.average_orbital_speed = average_orbital_speed
        self.mean_anomaly = mean_anomaly
        self.inclination_to_sun = inclination_to_sun
        self.inclination_to_invariable_plane = inclination_to_invariable_plane

    def __str__(self):
        return "Orbit({" \
               "aphelion: \"" + str(self.aphelion) + "\", "\
               "perihelion: \"" + str(self.perihelion) + "\", "\
               "semi_major_axis: \"" + str(self.semi_major_axis) + "\", "\
               "eccentricity: \"" + str(self.eccentricity) + "\", "\
               "orbital_period: \"" + str(self.orbital_period) + "\", "\
               "average_orbital_speed: \"" + str(self.average_orbital_speed) + "\", "\
               "mean_anomaly: \"" + str(self.mean_anomaly) + "\", "\
               "inclination_to_sun: \"" + str(self.inclination_to_sun) + "\", "\
               "inclination_to_invariable_plane: \"" + str(self.inclination_to_invariable_plane) + "\""\
               "})"
