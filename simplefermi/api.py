
from library import *
from distributions import *
import utils
from quantities import Quantity


def mean(q: Quantity) -> Quantity:
    return Quantity(np.mean(q.value), q.dimension)

def quantile(q: Quantity, p: float) -> Quantity:
    return Quantity(np.quantile(q.value, p), q.dimension)

def median(q: Quantity) -> Quantity:
    return Quantity(np.median(q.value), q.dimension)


