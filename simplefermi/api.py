
import pint
import uncertainties
from termcolor import colored
import numpy as np

from simplefermi import library
from simplefermi import distributions
from simplefermi import utils

One = library.dimensionless
Dimensionless = library.dimensionless

P = utils.P

def _quantity_repr(q: pint.Quantity) -> str:
    low, mid, high = np.quantile(q.magnitude, [(1-P)/2, 0.5, 1-(1-P)/2])
    rg = high - low

    result = f'{mid}'

    if rg:
        mid, low, high = utils.repr(q.magnitude)
        result = result + colored(f' ({low} to {high})', 'green')

    result = result + colored(f' [{q.units}]', 'blue')

    human_name = library.human_lookup(q.units)
    if human_name:
        result = result + colored(f' {{{human_name}}}', 'yellow')

    return result

library.ureg.Quantity.__repr__ = _quantity_repr