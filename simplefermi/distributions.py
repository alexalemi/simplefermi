"""Distributions are simple utility functions to generate random samples of various shapes."""

import math
import numpy as np
from pyerf import pyerf

from simplefermi.core import Q
from simplefermi import utils

from functools import partial

N = 200_000
P = utils.P 

def _unitize(vals, units=None):
    if units is None:
        return vals
    return Q(vals, units)

def _factor(x):
    return math.sqrt(2) * pyerf.erfinv(2 * x - 1)


## Normal Distributions

def plusminus(mean=0.0, sig=1.0, units=None, n=N):
    """Generates normally distributed random numbers with the given mean and standard deviation."""
    return _unitize(mean + sig * np.random.randn(n), units)

def normal(a, b, units=None, p=P, n=N):
    """A normal distribution with the given left and right endpoints."""
    mu = 0.5 * (a + b)
    factor = -_factor(0.5 * (1-p))
    sig = 0.5 * (b-a) / factor
    return _unitize(mu + sig * np.random.randn(n), units)


epsilon = partial(plusminus, mean=0.0, sig=1.0)

## Rectangles and triangles

def uniform(left, right, units=None, n=N):
    """A uniform, or rectangular distribution from the left to the right."""
    return _unitize(left + (right - left) * np.random.uniform(size=n), units)


def rectangular(center, width, units=None, n=N):
    """A rectangular distribution with the given center and width."""
    return _unitize(center +  width * (2 * np.random.uniform(size=n) - 1), units)

def triangular(center, width, units=None, right=None, n=N):
    """A triangular distribution, with two arguments is center and width and with three is center and left and right endpoint."""
    u = uniform(0, 1, n=n)
    c = center
    if right is None:
        a = c - width
        b = c + width 
    else:
        a = width
        b = right
    f = (c - a)/(b - a)
    return _unitize(np.where(
            u < f, 
            a + np.sqrt(u * (b - a) * (c - a)), 
            b - np.sqrt((1-u) * (b - a) * (b - c))), units)
    


## LogNormal

def lognormal(a, b, units=None, p=P, n=N):
    """A lognormal distribution with the given endpoints."""
    mu = np.log(np.sqrt(b * a))
    factor = -_factor(0.5 * (1-p))
    sig = np.log(np.sqrt(b/a))/factor
    return _unitize(np.exp(mu + sig * np.random.randn(n)), units)

def timesdivide(mean, rel_error, units=None, p=P, n=N):
    """A number with some relative error."""
    factor = -_factor(0.5 * (1-p))
    error = rel_error / factor
    return _unitize(np.exp(np.log(mean) + np.log(error) * np.random.randn(n)), units)

## Helper

def to(a, b, units=None, p=P, n=N):
    """Represent a range, uses lognormal if both are positive, normal otherwise."""
    if a > 0 and b > 0:
        return lognormal(a, b, units, p, n)
    else:
        return normal(a, b, units, p, n)

## Student and Gamma

def logstudent(a, b, units=None, df=2.0, p=P, n=N):
    """A logstudent distribution with left and right endpoints."""
    mu = np.log(np.sqrt(b * a))
    beta = np.sqrt(0.5 * (1 - p**2))/p
    sig = beta * np.log(np.sqrt(b/a))
    return _unitize(np.exp(mu + sig * np.random.standard_t(df, size=n)), units)

def gamma(a, units=None, n=N):
    """Give gamma distributed random numbers."""
    return _unitize(np.random.gamma(shape=a + 1, size=n), units)



## Twiddles

def percent(percentage, units=None, p=P, n=N):
    """Twiddles a result to within the given percentage. A times_divide type distribution."""
    top = 1.0 + percentage/100.0
    return _unitize(lognormal(1./top, top, p=p, n=N), units)


def db(x=1.0, units=None, p=P, n=N):
    """Gives a value with a certain uncertainty in decibels. ten decibels is an order of magnitude, 3 is a factor of 2."""
    return _unitize(lognormal(10**(-x/10.0), 10**(x/10.0), p=p, n=n), units)


## Fractions

def beta(a, b, units=None, n=N):
    return _unitize(np.random.beta(a+1, b+1, size=n), units)


def outof(frac, tot, units=None, n=N):
    return _unitize(np.random.beta(frac + 1, tot - frac + 1, size=n), units)


def against(a, b, units=None, n=N):
    return _unitize(np.random.beta(a, b, size=n), units)


## Data based

def data(values, weights=None, units=None, n=N):
    """Bootstraps a finite dataset."""
    if weights is not None:
        weights = np.asarray(weights)
        weights = weights / weights.sum()
    return _unitize(np.random.choice(values, size=N, replace=True, p=weights), units)

def mixture(*dists, weights=None, units=None, n=N):
    """Create a mixture of several sources."""
    if weights is None:
        return data([x for d in dists for x in data(d)], units=units, n=n)
    else:
        values, weights = zip(*[(x, w) for d, w in zip(dists, weights) for x in data(d)])
        return data(values, units=units, weights=weights, n=n)

def normalfit(values, units=None, n=N):
    return _unitize(plusminus(np.mean(values), np.std(values), n=n), units)

def sigfig(s, units=None):
    """Given a number as a string, generate the uniform distribution that accounts for the sigfigs."""
    return _unitize(plusminus(float(s), 0.5 * utils.sigfig_resolution(s)), units)


