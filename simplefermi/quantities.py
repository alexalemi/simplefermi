"""The main Quantity class."""

import operator
import functools
import numpy as np
import dimensions
import numbers


@functools.total_ordering
class Quantity(np.lib.mixins.NDArrayOperatorsMixin):
    _HANDLED_TYPES = (np.ndarray, numbers.Number)
    _CONFORMING_UFUNCS = (np.add, np.subtract, np.minimum, np.maximum)
    _NONLINEAR_UFUNCS = (np.sin, np.cos, np.tan, np.exp, np.log)
    _MAPPED_UFUNCS = (np.multiply, np.divide, np.floor_divide)

    def __init__(self, value, dimension):
        self.value = value
        self.dimension = dimension

    @property
    def dimensionless(self):
        return self.dimension.dimensionless

    def conforms(self, other):
        return self.dimension == other.dimension

    def __hash__(self):
        return hash((self.value, self.dimension))

    def __len__(self):
        return len(self.value)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # print(f"inside __array_ufunc__({ufunc}, {method}, {inputs}, {kwargs})")
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Quantity,)):
                return NotImplemented


        input_dimensions = tuple(x.dimension if isinstance(x, Quantity) else dimensions.DIMENSIONLESS
                         for x in inputs)
        inputs = tuple(x.value if isinstance(x, Quantity) else x
                        for x in inputs)
        if out:
            kwargs['out'] = tuple(
                    x.value if isinstance(x, Quantity) else x
                    for x in out)


        if ufunc in self._CONFORMING_UFUNCS:
            # check to make sure that all of the inputs have the same dimensions.
            assert functools.reduce(operator.eq, input_dimensions), f"Can only use {ufunc} on conforming quantities!"
            result_dimension = input_dimensions[0]
        elif ufunc in self._MAPPED_UFUNCS:
            result_dimension = getattr(ufunc, method)(*input_dimensions, **kwargs)
        elif ufunc in self._NONLINEAR_UFUNCS:
            assert all(x.dimensionless for x in input_dimensions), f"Can only use {ufunc} on dimensionless quantities!"
            result_dimension = input_dimensions[0]
        else:
            return NotImplemented

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x, result_dimension) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result, result_dimension)

    def __pow__(self, other):
        return Quantity(self.value ** other, self.dimension ** other)

    def __eq__(self, other):
        return (self.dimension == other.dimension) and (self.value == other.value)

    """
    def __lt__(self, other):
        assert self.conforms(other), "Can only compare conforming quantities!"
        return self.value < other.value

    def __add__(self, other):
        assert self.conforms(other), "Can only add conforming quantities!"
        return Quantity(self.value + other.value, self.dimension)

    def __sub__(self, other):
        assert self.conforms(other), "Can only subtract conforming quantities!"
        return Quantity(self.value - other.value, self.dimension)

    def __mul__(self, other):
        try:
            return Quantity(self.value * other.value, self.dimension * other.dimension)
        except AttributeError:
            return Quantity(self.value * other, self.dimension)

    def __rmul__(self, other):
        return Quantity(other * self.value, self.dimension)

    def __truediv__(self, other):
        try:
            return Quantity(self.value / other.value, self.dimension / other.dimension)
        except AttributeError:
            return Quantity(self.value / other, self.dimension)

    def __rtruediv__(self, other):
        return Quantity(other / self.value, self.dimension)

    def __floordiv__(self, other):
        try:
            return Quantity(self.value // other.value, self.dimension / other.dimension)
        except AttributeError:
            return Quantity(self.value // other, self.dimension)

    def __rfloordiv__(self, other):
        return Quantity(other // self.value, self.dimension)

    def __pow__(self, other):
        return Quantity(self.value ** other, self.dimension ** other)
    """

    def __repr__(self):
        return f"Q({self.value}, {self.dimension})"

