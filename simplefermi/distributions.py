
import numpy as np
import scipy.stats
from functools import partial

N = 200_000
P = 0.6826894


def plusminus(mean=0.0, sig=1.0, n=N):
    return mean + sig * np.random.randn(n)


epsilon = partial(plusminus, mean=0.0, sig=1.0)


def uniform(left, right, n=N):
    return left + (right - left) * np.random.uniform(n)


def normal(a, b, p=P, n=N):
    mu = 0.5 * (a + b)
    factor = scipy.stats.norm.ppf(0.5 * (1-p))
    sig = 0.5 * (b-a) / factor
    return mu + sig * np.random.randn(n)


def logstudent(a, b, df=2.0, p=P, n=N):
    mu = np.log(np.sqrt(b * a))
    beta = np.sqrt(0.5 * (1 - p**2))/p
    sig = beta * np.log(np.sqrt(b/a))
    return np.exp(mu + sig * np.random.standard_t(df, size=n))


def lognormal(a, b, p=P, n=N):
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
    if weights is not None:
        weights = np.asarray(weights)
        weights = weights / weights.sum()
    return np.random.choice(values, size=N, replace=True, p=weights)
