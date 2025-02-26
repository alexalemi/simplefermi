import pint
from io import BytesIO
from termcolor import colored
import numpy as np
import matplotlib.units
import base64
from PIL import Image

from simplefermi import core
from simplefermi import library
from simplefermi import utils
from simplefermi import dotplots

One = library.dimensionless
Dimensionless = library.dimensionless

P = utils.P
u = core.ureg


def repr(q: pint.Quantity) -> str:
    low, mid, high = np.quantile(q.magnitude, [(1 - P) / 2, 0.5, 1 - (1 - P) / 2])
    rg = high - low

    result = f"{mid}"

    if rg:
        mid, low, high = utils.repr(q.magnitude)
        result = f"{mid}" + colored(f" ({low} to {high})", "green")

    result = result + colored(f" [{q.units:~P}]", "blue")

    human_name = core.human_lookup(q.units)
    if human_name:
        result = result + colored(f" {{{human_name}}}", "yellow")

    return result


def html_repr(q: pint.Quantity) -> str:
    low, mid, high = np.quantile(q.magnitude, [(1 - P) / 2, 0.5, 1 - (1 - P) / 2])
    rg = high - low

    result = f"{mid}"

    if rg:
        mid, low, high = utils.repr(q.magnitude)
        result = f"{mid}" + f"<font color='green'> ({low} to {high})</font>"

    result = result + f"<font color='blue'> [{q.units:~P}]</font>"

    human_name = core.human_lookup(q.units)
    if human_name:
        result = result + f"<font color='orange'> {{{human_name}}}</font>"

    return result


def plain_repr(q: pint.Quantity) -> str:
    low, mid, high = np.quantile(q.magnitude, [(1 - P) / 2, 0.5, 1 - (1 - P) / 2])
    rg = high - low

    result = f"{mid}"

    if rg:
        mid, low, high = utils.repr(q.magnitude)
        result = f"{mid}" + f" ({low} to {high})"

    result = result + f" [{q.units:~}]"

    human_name = core.human_lookup(q.units)
    if human_name:
        result = result + f" {{{human_name}}}"

    return result


def _repr_pretty_(p: pint.Quantity, printer, cycle: bool):
    printer.text(repr(p))


core.ureg.Quantity._repr_latex_ = None
core.ureg.Quantity.__repr__ = plain_repr
core.ureg.Quantity._repr_pretty_ = _repr_pretty_


class QuantityConverter(matplotlib.units.ConversionInterface):
    @staticmethod
    def convert(value, unit, axis):
        "Convert a datetime value to a scalar or array."
        return value.to(unit).magnitude

    @staticmethod
    def axisinfo(unit, axis):
        "Return major and minor tick locators and formatters."
        return matplotlib.units.AxisInfo(label=str(unit))

    @staticmethod
    def default_units(x, axis):
        "Return the default unit for x or None."
        return x.to_base_units().units


matplotlib.units.registry[core.ureg.Quantity] = QuantityConverter()


def dotplot(q, quantiles=20, log=False, width=None, **circle_kwargs):
    if isinstance(q, core.ureg.Quantity):
        fig, axs = dotplots.dotplot(q.magnitude, quantiles, log, width, **circle_kwargs)
        label = f"{q.units:~P}"
        human_name = core.human_lookup(q.units)
        if human_name:
            label = label + f" {{{human_name}}}"
        axs.set_xlabel(label)
    else:
        fig, axs = dotplots.dotplot(q, quantiles, log, width, **circle_kwargs)
    return fig, axs


def _plotter(q: core.ureg.Quantity):
    with BytesIO() as b, matplotlib.pyplot.ioff():
        fig, axs = dotplot(q)
        fig.tight_layout()
        fig.savefig(b, format="png")
        matplotlib.pyplot.close(fig)
        return b.getvalue()


def plot(q: core.ureg.Quantity):
    b = BytesIO()
    with matplotlib.pyplot.ioff():
        fig, axs = dotplot(q)
        fig.tight_layout()
        fig.savefig(b, format="png")
        matplotlib.pyplot.close(fig)
        return Image.open(b)


def build_data_url(mimetype: str, data: bytes) -> str:
    # `data` must be base64 encoded
    str_repr = data.decode("utf-8").replace("\n", "")
    return f"data:{mimetype};base64,{str_repr}"


def _mime_(q: core.ureg.Quantity):
    plot_bytes = base64.b64encode(_plotter(q))
    data_url = build_data_url("image/png", plot_bytes)
    return ("text/html", f"{html_repr(q)}<br><img src='{data_url}' />")


core.ureg.Quantity.plot = plot
core.ureg.Quantity._repr_png_ = _plotter
core.ureg.Quantity._mime_ = _mime_
core.ureg.Quantity._repr_html_ = lambda self: _mime_(self)[1]
