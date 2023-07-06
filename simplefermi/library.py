"""Defines the basic quantities and units and things that are unique to this package."""

import math
import sys

_this_module = sys.modules[__name__]

import pint


from simplefermi.distributions import data, plusminus

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


m = ureg.m
s = ureg.s
kg = ureg.kg
A = ureg.A
K = ureg.K
mol = ureg.mol
bit = ureg.bit
cd = ureg.cd
dimensionless = ureg.dimensionless
uno = 1.0 * dimensionless
J = ureg.J
coulomb = ureg.coulomb
C = coulomb
N = ureg.newton
volt = ureg.volt
V = volt
ohm = ureg.ohm
siemens = ureg.siemens
weber = ureg.weber
henry = ureg.henry
tesla = ureg.tesla
T = tesla
watt = ureg.watt
day = ureg.day

ten = 10
kilo = 1000

store(m, 'length')
store(s, 'time')
store(kg, 'mass')
store(A, 'current')
store(K, 'temperature')
dollar = make("dollar")
store(dollar, 'currency')
store(mol, 'amount of substance')
store(bit, 'information')
store(cd, 'luminous intensity')
store(dimensionless, 'dimensionless')
store(m**2, 'area')
store(m**3, 'volume')
store(s**-1, 'frequency')
store(m*s**-1, 'velocity')
store(m*s**-2, 'acceleration')
store(m*kg*s**-1, 'momentum')
store(m*kg*s**-2, 'force')
store(m**2*kg*s**-3, 'power')
store(m**-1*kg*s**-2, 'pressure')
store(m**2*kg*s**-2, 'energy')
store(m**2*kg*s**-1, 'angular momentum')
store(m**2*kg, 'moment of inertia')
store(m**3*s**-1, 'flow')
store(m**-3*kg, 'mass density')
store(m**3*kg**-1, 'specific volume')
store(A*m**-2, 'electric current density')
store(dollar*kg**-1, 'price per mass')

store(J*m**-2, 'surface tension')

store(coulomb, 'charge')
store(coulomb*m**-2, 'surface charge density')
store(coulomb*m**-3, 'electric charge density')

store(volt, 'electric potential')
store(V / m, 'electric field strength')
store(A / m, 'magnetic field strength')

store(ohm, 'electric resistance')

store(siemens, 'electric conductance')

store(weber, 'magnetic flux')
store(henry, 'inductance')

store(tesla, 'magnetic flux density')
store(J/K, 'heat capacity')
store(J*kg**-1*K**-1, 'specific heat capacity')
lumen = ureg.lumen

## populate from pint

for name in ureg:
    if name in ureg:
        setattr(_this_module, name, ureg[name])

## Mathematical constants

googol = ten**100
pi = math.pi
e = math.e
tau = math.tau

# New 2019 SI base units

h = Planck = planck = plancks_constant = 6.626_070_15e-34 * (J * s)
elementary_charge = 1.602_176_634e-19 * C
k = boltzmann = boltzmann_constant = boltzmanns_constant = 1.380_649e-23 * (J / K)
NA = avogadro = 6.022_140_76e23 * (mol**-1)
c = speed_of_light = 299_792_458 * (m / s)
vcs = 9_192_631_770 * (s**-1)
kcd = 683 * (lumen / watt)

# CODATA Physical constants

# c = speed_of_light = constants.c * m / s
# elementary_charge = plusminus(1.6021766208e-19, 0.0000000098e-19) * C
# h = plusminus(6.626070040e-34, 0.000000081e-34) * (J * s)
hbar = h / (2 * pi)
classical_electron_radius = plusminus(2.8179403227e-15, 0.0000000019e-15) * m
thomson_cross_section = plusminus(
    0.66524587158e-28, 0.00000000091e-28) * (m**2)
G = plusminus(6.67408e-11, 0.00031e-11) * (N * m**2 / kg**2)
standard_gravity = 9.80662 * m / s**2
atomic_mass_unit = plusminus(1.660539040e-27, 0.000000020e-27) * kg
# avogadro = plusminus(6.022140857e23, 0.000000074e23) * (mol**-1)
# gas_constant = plusminus(8.3144598, 0.0000048) * (J / (mol * K))
# boltzmann = plusminus(1.38064852e-23, 0.00000079e-23) * J/K
wien_displacement = plusminus(2.8977729e-3, 0.0000017e-3) * (m * K)
# alpha = plusminus(7.2973525664e-3, 0.0000000017e-3) * dimensionless
Rydberg_constant = plusminus(10973731.568508, 0.000065) * (m**-1)
bohr_radius = plusminus(0.52917721067e-10, 0.00000000012e-10) * m
planck_temperature = plusminus(1.416808e32, 0.000033e32) * K
muon_magnetic_moment = plusminus(-4.49044826e-26, 0.00000010e-26) * (J/T)
proton_magnetic_moment = plusminus(1.4106067873e-26, 0.0000000097e-26) * (J/T)
electron_magnetic_moment = plusminus(-928.4764520e-26, 0.0000057e-26) * (J/T)
neutron_magnetic_moment = plusminus(-0.96623650e-26, 0.00000023e-26) * (J/T)
deuteron_magnetic_moment = plusminus(
    0.4330735040e-26, 0.0000000036e-26) * (J/T)

## Derived values

# mu0 = 2 * alpha * h / (elementary_charge**2 * c)
# epsilon0 = 1/(mu0 * c**2)
R = gas_constant = avogadro * boltzmann


# DATA

earth_mass = plusminus(5.9722e24, 6.0e20) * kg
earth_radius = plusminus(6371, 10) * kilo * m
sigma = stefan_boltzmann = 2 * pi**5 * boltzmann**4 / (15 * c**2 * h**3)
solar_constant = plusminus(1.3608, 0.0005) * kilo * watt / m**2

# In the gregorian calendar, the calendar cycles every 400 years.
year = data(values=[365, 366], weights=[303, 97]) * day
# 303 are 365, 97 are leap years with 366 days.
yr = year

month = data(values=[31, 29, 30, 28], weights=[2800, 97, 1600, 303]) * day
# Using the same math above, in a 400 year cycle the calendar repeats.
