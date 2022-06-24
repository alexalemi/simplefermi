
import sys

from quantities import Quantity
from library import human_lookup
from distributions import P
import utils

import numpy as np

_BLUE = '\001\x1b[34m\002'
_GREEN = '\001\x1b[32m\002'
_YELLOW = '\001\x1b[33m\002'
_CYAN = '\001\x1b[36m\002'
_RESET = '\001\x1b[0m\002'
_RED = '\001\x1b[31m\002'
_GREY = '\001\x1b[90m\002' 

ALPHA = P

from math import floor, log10

def median(sorted_vals):
    size = len(sorted_vals)
    if size % 2 == 1:
        return sorted_vals[(size+1)//2]
    else:
        return 0.5 * (sorted_vals[size // 2] + sorted_vals[size // 2 + 1])


def interval(sorted_vals, alpha=ALPHA):
    """Gives the interval for a sorted set of values."""
    size = len(sorted_vals)
    cut = int(size * alpha/2.)
    if cut < 10:
        return sorted_vals[0], sorted_vals[-1]
    return sorted_vals[cut], sorted_vals[-cut]


def shortest_interval(sorted_vals, alpha=ALPHA):
    """Gives the shortest interval for a sorted set of values."""
    size = len(sorted_vals)
    cut = int(size * (1-alpha))
    if cut < 10:
        return sorted_vals[0], sorted_vals[-1]
    left = size - cut
    start = (sorted_vals[-left:] - sorted_vals[:left]).argmin()
    return sorted_vals[start], sorted_vals[start+cut]

def magnitude(x):
    """Return the decimal points of magnitude."""
    if x == 0:
      return 3
    return int(floor(log10(abs(x))))

def round_sig(x, sig=2):
    """Round to the given significant digits."""
    return round(x, sig-magnitude(x)-1)

def round_mag(x, mag=1):
    return round(x, mag)

def repr_sig(x, sig=2):
  if sys.version_info[0] > 2:
    return "{{:#,.0{}g}}".format(sig).format(x)
  else:
    return "{{:,.0{}g}}".format(sig).format(x)

def repr_mag(x, mag=0, padding=2):
  sig = max(-mag+magnitude(x)+padding, 0)
  x = round_sig(x, sig)
  if sys.version_info[0] > 2:
    return "{{:#,.0{}g}}".format(sig).format(x)
  else:
    return "{{:,.0{}g}}".format(sig).format(x)

def round_repr(center, left, right, padding=2):
    mag = magnitude(right - left)
    return (repr_mag(center, mag), repr_mag(left, mag), repr_mag(right, mag))

def repr(sorted_values, padding=2):
    left, right = interval(sorted_values)
    center = median(sorted_values)
    mag = magnitude(right - left)
    return (repr_mag(center, mag, padding=padding),
            repr_mag(left, mag, padding=padding),
            repr_mag(right, mag, padding=padding))

def sigfig_resolution(number_string):
  """Given a number as a string, return a string with the sigfig width.

  For Example:
        3.323e4     to  1.
        -3.323e4    to  -0.001e4
        -3.323e004  to  -0.001e004
        -3.323e-004 to  -0.001e-004
        -3.323E-004 to  -0.001E-004
        2342e3      to  1.0e3
        -2342e3     to  -1e3
        -2342e-3    to  -1e-3
        234.04      to  000.01
  """
  # Split the number into relevant pieces, zero out all but the last nonzero digit, and then
  # divide by 10.0
  #  0: sign  1: numbers  2. zeros 3: dot  4: digits 5: exponent
  pat = r'^([+-]?)(\d*?)(0*)(\.)?(\d*)([eE][-=]?\d+)?$'

  # Special case, if the input is zero, return zero 
  if float(number_string) == 0.0:
    return 0.0

  groups = list(re.match(pat, number_string).groups())
  if groups[3]:
      # if the number contains a decimal
      if groups[4]:
          # if there are any numbers to the right of the decimal
          # zero out the leading numbers
          groups[1] = ''.join('0' for x in groups[1]) or ''
          groups[4] = ''.join('0' for x in groups[4]) or ''
          groups[4] = groups[4][:-1] + '1'
      else:
          # Unit zero
          return float(1.0)
  else:
      # Doesn't contain a decimal, just do the last nonzero, but using a new pattern
      #  0: sign  1: numbers  2. zeros 3: dot  4: digits 5: exponent
      pat = r'^([+-]?)(\d*?)(0*)([eE][-=]?\d+)?$'
      groups = list(re.match(pat, number_string).groups())
      groups[1] = ''.join('0' for x in groups[1]) or ''
      groups[1] = groups[1][:-1] + '1'

  groups = [(x or '') for x in groups]
  return float(''.join(groups))


def _quantity_repr(q: Quantity) -> str:
    low, mid, high = np.quantile(q.value, [(1-P)/2, 0.5, 1-(1-P)/2])
    rg = high - low

    result = f"{mid}"

    if rg:
        # mid, low, high = utils.repr(list(sorted(q.value)))
        result = f"{mid} {_GREEN}({low} to {high}){_RESET}"

    result = f"{result} {_BLUE}[{q.dimension}]{_RESET}"

    if human_name := human_lookup(q.dimension):
        result = f"{result} {_YELLOW}{{{human_name}}}{_RESET}"
    
    return result

Quantity.__repr__ = _quantity_repr
