"""Distributions are simple utility functions to generate random samples of various shapes."""

import numpy as np
import scipy.stats

from simplefermi import utils

from functools import partial

N = 200_000
P = utils.P 


def plusminus(mean=0.0, sig=1.0, n=N):
    """Generates normally distributed random numbers with the given mean and standard deviation."""
    return mean + sig * np.random.randn(n)


epsilon = partial(plusminus, mean=0.0, sig=1.0)


def uniform(left, right, n=N):
    """A uniform, or rectangular distribution from the left to the right."""
    return left + (right - left) * np.random.uniform(size=n)


def rectangular(center, width, n=N):
    """A rectangular distribution with the given center and width."""
    return center +  width * (2 * np.random.uniform(size=n) - 1)


def normal(a, b, p=P, n=N):
    """A normal distribution with the given left and right endpoints."""
    mu = 0.5 * (a + b)
    factor = scipy.stats.norm.ppf(0.5 * (1-p))
    sig = 0.5 * (b-a) / factor
    return mu + sig * np.random.randn(n)


def logstudent(a, b, df=2.0, p=P, n=N):
    """A logstudent distribution with left and right endpoints."""
    mu = np.log(np.sqrt(b * a))
    beta = np.sqrt(0.5 * (1 - p**2))/p
    sig = beta * np.log(np.sqrt(b/a))
    return np.exp(mu + sig * np.random.standard_t(df, size=n))


def lognormal(a, b, p=P, n=N):
    """A lognormal distribution with the given endpoints."""
    mu = np.log(np.sqrt(b * a))
    factor = scipy.stats.norm.ppf(0.5 * (1-p))
    sig = np.log(np.sqrt(b/a))/factor
    return np.exp(mu + sig * np.random.randn(n))


def beta(a, b, n=N):
    return np.random.beta(a+1, b+1, size=n)


def outof(frac, tot, n=N):
    return np.random.beta(frac + 1, tot - frac + 1, size=n)


def against(a, b, n=N):
    return np.random.beta(a, b, size=n)


def data(values, weights=None, n=N):
    """Bootstraps a finite dataset."""
    if weights is not None:
        weights = np.asarray(weights)
        weights = weights / weights.sum()
    return np.random.choice(values, size=N, replace=True, p=weights)


def normalfit(values, n=N):
    return plusminus(np.mean(values), np.std(values), n=n)


def triangular(center, width, right=None, n=N):
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
    return np.where(
            u < f, 
            a + np.sqrt(u * (b - a) * (c - a)), 
            b - np.sqrt((1-u) * (b - a) * (b - c)))
    

def gamma(a, n=N):
    """Give gamma distributed random numbers."""
    return np.random.gamma(shape=a + 1, size=n)


def sigfig(s):
    """Given a number as a string, generate the uniform distribution that accounts for the sigfigs."""
    return plusminus(float(s), 0.5 * utils.sigfig_resolution(s))
