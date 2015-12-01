from math import *

MAX_ITERATIONS = 100

gravitational_constant = 6.67408 * 10 ** -20


class ConvergenceError(Exception):
    pass


def eccentric_anomaly_from_mean(e, M, tolerance=1e-14):
    """
    Convert mean anomaly to eccentric anomaly.
    Implemented from [A Practical Method for Solving the Kepler Equation][1]
    by Marc A. Murison from the U.S. Naval Observatory
    [1]: http://murison.alpheratz.net/dynamics/twobody/KeplerIterations_summary.pdf
    """

    Mnorm = fmod(M, 2 * pi)
    E0 = M + (-1 / 2 * e ** 3 + e + (e ** 2 + 3 / 2 * cos(M) * e ** 3) * cos(M)) * sin(M)
    dE = tolerance + 1
    count = 0
    while dE > tolerance:
        t1 = cos(E0)
        t2 = -1 + e * t1
        t3 = sin(E0)
        t4 = e * t3
        t5 = -E0 + t4 + Mnorm
        t6 = t5 / (1 / 2 * t5 * t4 / t2 + t2)
        E = E0 - t5 / ((1 / 2 * t3 - 1 / 6 * t1 * t6) * e * t6 + t2)
        dE = abs(E - E0)
        E0 = E
        count += 1
        if count == MAX_ITERATIONS:
            raise ConvergenceError('Did not converge after {n} iterations. (e={e!r}, M={M!r})'.format(n=MAX_ITERATIONS, e=e, M=M))
    return E


def true_anomaly_from_eccentric(e, E):
    """
    Convert eccentric anomaly to true anomaly.
    """

    return 2 * atan2(sqrt(1 + e) * sin(E / 2), sqrt(1 - e) * cos(E / 2))
