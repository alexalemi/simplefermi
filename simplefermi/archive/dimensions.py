"""Module for handing units in fermi."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from builtins import str, dict, object

import functools
import numbers


def _inc(dictionary, symbol, power=1):
    dictionary[symbol] = dictionary.get(symbol, 0) + power
    return dictionary


def _dec(dictionary, symbol, power=1):
    _inc(dictionary, symbol, -power)
    return dictionary


@functools.total_ordering
class Symbol(object):
    """Represents a Symbol."""

    def __init__(self, name):
        self.name = name

    def as_dimension(self):
        """Convert to a Dimension."""
        return Dimension({self: 1})

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __pow__(self, power):
        assert isinstance(power, numbers.Rational), "Can only raise to numeric powers."
        return Dimension({self: power})

    def __mul__(self, other):
        dictionary = {self: 1}
        if isinstance(other, Symbol):
            _inc(dictionary, other)
            return Dimension(dictionary)
        if isinstance(other, Dimension):
            for symbol, power in other:
                _inc(dictionary, symbol, power)
            return Dimension(dictionary)
        raise TypeError("Can only multiple Symbols by other Symbols or Dimensions.")

    def __rtruediv__(self, other):
        dictionary = {self: -1}
        if isinstance(other, int):
            if other != 1:
                raise TypeError("Cannot divide numbers and Dimensions. (only 1)")
        else:
            raise TypeError("Can only divide Symbols by other Symbols or Dimensions.")
        return Dimension(dictionary)

    def __truediv__(self, other):
        dictionary = {self: 1}
        if isinstance(other, Symbol):
            _dec(dictionary, other)
        elif isinstance(other, Dimension):
            for symbol, power in other:
                _dec(dictionary, symbol, power)
        else:
            raise TypeError("Can only multiple Symbols by other Symbols or Dimensions.")
        return Dimension(dictionary)


class Dimension(object):
    """Represents the Dimension part of the Quantity."""

    def __init__(self, dictionary):
        self._dict = dict(dictionary)
        self.simplify()

    @classmethod
    def make(cls, s):
        return cls({Symbol(s): 1})

    @property
    def dimensionless(self):
        """Is a pure number."""
        return not self._dict

    def __eq__(self, other):
        return dict(iter(self)) == dict(iter(other))

    def conforms(self, other):
        return self == other

    def __iter__(self):
        return iter(self._dict.items())

    def __hash__(self):
        return hash(tuple(sorted(self)))

    def simplify(self):
        """Remove unused base units."""
        self._dict = {
            symbol: power for symbol, power in self._dict.items() if power != 0
        }
        return self

    def __pow__(self, other):
        try:
            if other.dimensionless:
                other = other.distribution
        except AttributeError:
            pass

        new_dict = {symbol: power * other for symbol, power in self}
        return self.__class__(new_dict)

    def __mul__(self, other):
        new_dict = self._dict.copy()
        if isinstance(other, Symbol):
            _inc(new_dict, other)
        elif isinstance(other, Dimension):
            for symbol, power in other:
                _inc(new_dict, symbol, power)
        else:
            raise TypeError(
                "Can only multiply Dimensions by Symbols or other Dimensions."
            )
        return self.__class__(new_dict)

    def __truediv__(self, other):
        new_dict = self._dict.copy()
        if isinstance(other, Symbol):
            _dec(new_dict, other)
        elif isinstance(other, Dimension):
            for symbol, power in other:
                _dec(new_dict, symbol, power)
        else:
            try:
                for symbol, power in other.dimension:
                    _dec(new_dict, symbol, power)
            except AttributeError:
                raise TypeError(
                    "Can only divide Dimensions by Symbols or other Dimensions."
                )
        return self.__class__(new_dict)

    __floordiv__ = __truediv__

    def __rtruediv__(self, other):
        dictionary = {symbol: -power for symbol, power in self}
        if isinstance(other, int):
            if other != 1:
                raise TypeError("Cannot divide numbers and Dimensions. (only 1)")
        else:
            raise TypeError("Can only multiple Symbols by other Symbols or Dimensions.")
        return Dimension(dictionary)

    def __repr__(self):
        def _format(symbol, power):
            if power == 1:
                return repr(symbol)
            return "%r^%s" % (symbol, power)

        if self.dimensionless:
            return "1"

        return " ".join([_format(symbol, power) for symbol, power in iter(self)])


def as_dimension(x):
    if isinstance(x, Symbol):
        return x.as_dimension()
    if isinstance(x, Dimension):
        return x
    raise TypeError("Only Symbols and Dimensions can be promoted to Dimensions.")


DIMENSIONLESS = Dimension({})
