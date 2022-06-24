
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


One = Q(1, DIMENSIONLESS)
