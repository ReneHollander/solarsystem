from math import fmod, cos, sin, pi, atan2, sqrt

MAX_ITERATIONS = 100

gravitational_constant = 6.67408 * 10 ** -11


class ConvergenceError(Exception):
    pass


def eccentric_anomaly_from_mean(e, M, tolerance=1e-14):
    """
    Convert mean anomaly to eccentric anomaly.
    Implemented from [A Practical Method for Solving the Kepler Equation][1]
    by Marc A. Murison from the U.S. Naval Observatory
    [1]: http://murison.alpheratz.net/dynamics/twobody/KeplerIterations_summary.pdf
    """

    Mnorm = fmod(M, 2.0 * pi)
    E0 = M + (-1 / 2.0 * e ** 3.0 + e + (e ** 2.0 + 3.0 / 2.0 * cos(M) * e ** 3.0) * cos(M)) * sin(M)
    dE = tolerance + 1
    count = 0
    while dE > tolerance:
        t1 = cos(E0)
        t2 = -1 + e * t1
        t3 = sin(E0)
        t4 = e * t3
        t5 = -E0 + t4 + Mnorm
        t6 = t5 / (1.0 / 2.0* t5 * t4 / t2 + t2)
        E = E0 - t5 / ((1.0 / 2.0 * t3 - 1.0 / 6.0 * t1 * t6) * e * t6 + t2)
        dE = abs(E - E0)
        E0 = E
        count += 1.0
        if count == MAX_ITERATIONS:
            raise ConvergenceError('Did not converge after {n} iterations. (e={e!r}, M={M!r})'.format(n=MAX_ITERATIONS, e=e, M=M))
    return E


def true_anomaly_from_eccentric(e, E):
    """
    Convert eccentric anomaly to true anomaly.
    """

    return 2 * atan2(sqrt(1.0 + e) * sin(E / 2.0), sqrt(1.0 - e) * cos(E / 2.0))
