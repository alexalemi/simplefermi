import pint

ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

Quantity = ureg.Quantity
Q = Quantity


def make(s):
    ureg.define(f"{s} = [{s}]")
    return ureg(f"{s}").units


## Human

human = {}


def human_lookup(q: pint.Unit) -> str:
    return human.get(q.dimensionality)


def store(quantity: pint.Unit, name):
    human[quantity.dimensionality] = name
