
import pint
import uncertainties
from termcolor import colored

from simplefermi.library import *
from simplefermi.distributions import *
from simplefermi import utils

One = dimensionless
Dimensionless = dimensionless

def _quantity_repr(q: pint.Quantity) -> str:
    low, mid, high = np.quantile(q.magnitude, [(1-P)/2, 0.5, 1-(1-P)/2])
    rg = high - low

    result = f'{mid}'

    if rg:
        mid, low, high = utils.repr(q.magnitude)
        result = result + colored(f' ({low} to {high})', 'green')

    result = result + colored(f' [{q.units}]', 'blue')

    human_name = human_lookup(q.units)
    if human_name:
        result = result + colored(f' {{{human_name}}}', 'yellow')

    return result

ureg.Quantity.__repr__ = _quantity_repr