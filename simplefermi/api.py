
from simplefermi.library import *
from simplefermi.distributions import *
import simplefermi.utils
from simplefermi.quantities import Quantity


def mean(q: Quantity) -> Quantity:
    return Quantity(np.mean(q.value), q.dimension)

def quantile(q: Quantity, p: float) -> Quantity:
    return Quantity(np.quantile(q.value, p), q.dimension)

def median(q: Quantity) -> Quantity:
    return Quantity(np.median(q.value), q.dimension)


