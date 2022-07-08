
from simplefermi.library import *
from simplefermi.distributions import *
from simplefermi import utils
from simplefermi.quantities import Quantity


def mean(q: Quantity) -> Quantity:
    return Quantity(np.mean(q.value), q.dimension)


def quantile(q: Quantity, p: float) -> Quantity:
    return Quantity(np.quantile(q.value, p), q.dimension)


def median(q: Quantity) -> Quantity:
    return Quantity(np.median(q.value), q.dimension)


def sigfig(s):
    return plusminus(float(s), 0.5 * utils.sigfig_resolution(s))


def percent(val, error):
    return plusminus(val, error * val)


def accuracy(q: Quantity) -> float:
    left, mid, right = np.quantile(q.value, [(1-P)/2, 1/2, 1-(1-P)/2])
    return (right - left) / 2 / mid

def triangular(center, width, right=None):
    u = uniform(0, 1)
    c = center
    if right is None:
        a = c - width
        b = c + width 
    else:
        a = width
        b = right
    f = (c - a)/(b - a)
    return np.where(
            u < f, 
            a + np.sqrt(u * (b - a) * (c - a)), 
            b - np.sqrt((1-u) * (b - a) * (b - c)))



One = Q(1, DIMENSIONLESS)
