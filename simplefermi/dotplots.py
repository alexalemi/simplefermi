
import math
import numpy as np
from matplotlib import rc, patches
import matplotlib.pyplot as plt


def smoothing(v, thres):
    n = len(v)
    a = 0
    b = 1

    # get left stack
    while v[a] == v[b]:
        b += 1

    while (b < n):
        # get right stack
        c = b + 1
        while c < n and v[b] == v[c]:
            c += 1

        # are stacks adjacent?
        # if so, compare sizes and swap as needed
        if ((v[b] - v[b-1]) < thres):
            d = b + ((a + c - b - b) >> 1)
            while (d < b):
                v[d] = v[b]
                d += 1
            while (d > b):
                v[d] = v[a]
                d -= 1

        a = b
        b = c

    return v


def dotbin(array, step, smooth=False, f=None):
    if f is None:
        def f(x): return x
    n = len(array)
    v = np.zeros(n)

    i = 0
    j = 1
    a = f(array[0])
    b = a
    w = a + step

    while j < n:
        x = f(array[j])
        if (x >= w):
            b = (a + b) / 2
            while i < j:
                v[i] = b
                i += 1
            w = x + step
            a = x
        b = x
        j += 1

    b = (a + b) / 2
    while i < j:
        v[i] = b
        i += 1

    if smooth:
        return smoothing(v, step + step / 4)
    return v


def circle(fig, ax, xy, radius, kwargs=None):
    """Create circle on figure with axes of different sizes.

    Plots a circle on the current axes using `plt.Circle`, taking into account
    the figure size and the axes units.

    It is done by plotting in the figure coordinate system, taking the aspect
    ratio into account. In this way, the data dimensions do not matter.
    However, if you adjust `xlim` or `ylim` after plotting `circle`, it will
    screw them up; set `plt.axis` before calling `circle`.

    Parameters
    ----------
    xy, radius, kwars :
        As required for `plt.Circle`.
    """

    # Calculate figure dimension ratio width/height
    pr = fig.get_figwidth()/fig.get_figheight()

    # Get the transScale (important if one of the axis is in log-scale)
    tscale = ax.transScale + (ax.transLimits + ax.transAxes)
    ctscale = tscale.transform_point(xy)
    cfig = fig.transFigure.inverted().transform(ctscale)

    # Create circle
    if kwargs == None:
        circ = patches.Ellipse(cfig, radius, radius*pr,
                               transform=fig.transFigure)
    else:
        circ = patches.Ellipse(cfig, radius, radius*pr,
                               transform=fig.transFigure, **kwargs)

    # Draw circle
    ax.add_artist(circ)


def padinterval(interval, f=0.05):
    left, right = interval
    range = right - left
    return left - f * range, right + f * range


def placedots(fig, ax, array, width, **circle_kwargs):
    last = None
    height = 0.5 * width
    artists = []
    maxheight = height
    for value in array:
        if (value == last):
            height += width
            if height > maxheight:
                maxheight = height
        else:
            height = 0.5 * width
            last = value
        # circle(fig, ax, (value, height), radius=width/2.0)
        circle = plt.Circle((value, height), radius=width/2.0, linewidth=2, edgecolor='k', **circle_kwargs)
        ax.add_artist(circle)
    ax.set_xlim(padinterval((min(array) - width/2.0, max(array) + width/2.0)))
    ax.set_ylim(padinterval((0, maxheight + width/2.0)))


def dotplot(arr, quantiles=20, log=False, width=None, figsize=(3,2), **circle_kwargs):
    n = quantiles
    qs = np.arange(0.5/n, 1, 1/n)
    if log:
        quantiles = np.quantile(np.log10(arr), qs)
    else:
        quantiles = np.quantile(arr, qs)

    fig, axs = plt.subplots(figsize=figsize)
    axs.set_yticks([])
    axs.set_aspect('equal')

    if width is None:
        width = 5/2 * (quantiles.max() - quantiles.min())/n
    dotlocs = dotbin(quantiles, width, False)
    placedots(fig, axs, dotlocs, width, **circle_kwargs)

    return fig, axs
