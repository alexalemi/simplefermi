
# from fractions import Fraction

from simplefermi.dimensions import Dimension, DIMENSIONLESS
from simplefermi.quantities import Quantity
from simplefermi.distributions import data, plusminus

human = {}
human_lookup = human.get

def store(quantity, name):
    human[quantity.dimension] = name

## API

Q = Quantity
one = 1  # Fraction(1, 1)

def make(s: str) -> Quantity:
    return Q(one, Dimension.make(s))

## Prefixes

ten = 10  # Fraction(10, 1)
hella =   ten**27                   ## 1E27 Californian hella, "lots"
yotta =   ten**24                   ## 1E24 Greek or Latin octo, "eight"
zetta =   ten**21                   ## 1E21 Latin septem, "seven"
exa   =   ten**18                   ## 1E18 Greek hex, "six"
peta  =   ten**15                   ## 1E15 Greek pente, "five"
tera  =   ten**12                   ## 1E12 Greek teras, "monster"
giga  =   ten**9                    ## 1E9  Greek gigas, "giant"
mega  =   ten**6                    ## 1E6  Greek megas, "large"
myria =   ten**4                    ## 1E4  Not an official SI prefix
kilo  =   ten**3                    ## 1E3  Greek chilioi, "thousand"
hecto =   ten**2                    ## 1E2  Greek hekaton, "hundred"
deca  =   ten                       ## 1E1  Greek deka, "ten"
deka  =   ten
deci  =   ten**-1                   ## 1E-1 Latin decimus, "tenth"
centi =   ten**-2                   ## 1E-2 Latin centum, "hundred"
milli =   ten**-3                   ## 1E-3 Latin mille, "thousand"
micro =   ten**-6                   ## 1E-6 Latin micro/Greek mikros,"small"
nano  =   ten**-9                   ## 1E-9 Latin nanus or Greek nanos,"dwarf"
pico  =   ten**-12                  ## 1E-12 Spanish pico, "a bit"
femto =   ten**-15                  ## 1E-15 Danish-Norwegian femten,"fifteen"
atto  =   ten**-18                  ## 1E-18 Danish-Norwegian atten,"eighteen"
zepto =   ten**-21                  ## 1E-21 Latin septem, "seven"
yocto =   ten**-24                  ## 1E-24 Greek or Latin octo, "eight"

Y =   yotta
Z =   zetta
E =   exa
P =   peta
T =   tera
G =   giga
M =   mega
k =   kilo
h =   hecto
da =  deka
d =   deci
c =   centi
m =   milli
n =   nano
p =   pico
f =   femto
a =   atto
z =   zepto
y =   yocto

## SI units

m = make("m")
store(m, "length")
meter = m

s = make("s")
store(s, "time")
second = s

kg = make("kg")
store(kg, "mass")
kilogram = kg
gram = kg * milli

A = make("A")
store(A, "current")
ampere = A
amp = ampere

K = make("K")
store(K, "temperature")
kelvin = K

dollar = make("dollar")
store(dollar, "currency")

mol = make("mol")
store(mol, "amount of substance")
mole = mol
radian = 1
sr = 1
steradian = sr

bit = make("bit")
store(bit, "information")

cd = make("cd")
store(cd, "luminous intensity")
candela = cd


## Unit Combinations

store(Q(1, DIMENSIONLESS), "dimensionless")

store(m**2, "area")
store(m**3, "volume")

store(s**-1, "frequency")

store(m*s**-1, "velocity")
store(m*s**-2, "acceleration")
store(m*kg*s**-1, "momentum")

store(m*kg*s**-2, "force")
store(m**2*kg*s**-3, "power")
store(m**-1*kg*s**-2, "pressure")
store(m**2*kg*s**-2, "energy")
store(m**2*kg*s**-1, "angular momentum")
store(m**2*kg, "moment of inertia")

store(m**3*s**-1, "flow")

store(m**-3*kg, "mass density")
store(m**3*kg**-1, "specific volume")

store(A*m**-2, "electric current density")

store(dollar*kg**-1, "price per mass")


## Some Numbers

semi    =  1/2
demi    =  1/2
hemi    =  1/2
half    =   1/2
third   =   1/3
quarter =   1/4
eighth  =   1/8

uni =    1
bi =     2
tri =    3

zero =                0
one =                 1
two =                 2
double =              2
three =               3
triple =              3
treble =              3
four =                4
quadruple =           4
five =                5
quintuple =           5
six =                 6
sextuple =            6
seven =               7
septuple =            7
eight =               8
nine =                9
ten =                 10
twenty =              20
thirty =              30
forty =               40
fifty =               50
sixty =               60
seventy =             70
eighty =              80
ninety =              90

hundred =             100
thousand =            1000
million =             ten**6
billion =             ten**9
trillion =            ten**12
quadrillion =         ten**15
quintillion =         ten**18
sextillion =          ten**21
septillion =          ten**24
octillion =           ten**27
nonillion =           ten**30
noventillion =        nonillion
decillion =           ten**33
undecillion =         ten**36
duodecillion =        ten**39
tredecillion =        ten**42
quattuordecillion =   ten**45
quindecillion =       ten**48
sexdecillion =        ten**51
septendecillion =     ten**54
octodecillion =       ten**57
novemdecillion =      ten**60
vigintillion =        ten**63
centillion =          ten**303

googol = ten**100


## Named SI Derived units

newton = kg * m / s**2
N = newton
pascal = N/m**2
Pa = pascal
joule = N * m
J = joule
watt = J/s
W = watt

store(J*m**-2, "surface tension")

coulomb = A*s
store(coulomb, "charge")
store(coulomb*m**-2, "surface charge density")
store(coulomb*m**-3, "electric charge density")
C = coulomb

volt = W/A
V = volt
store(volt, "electric potential")
store(V / m, "electric field strength")
store(A / m, "magnetic field strength")

ohm = V / A
store(ohm, "electric resistance")

siemens = A/V
S = siemens
store(siemens, "electric conductance")

farad = C/V

F = farad
uF = farad*micro

weber = V * s
store(weber, "magnetic flux")
Wb = weber

henry = Wb / A
store(henry, "inductance")
henries = henry
H = henry

tesla = Wb / m**2
store(tesla, "magnetic flux density")
T = tesla

hertz = s**-1
Hz = hertz

store(J/K, "heat capacity")
store(J*kg**-1*K**-1, "specific heat capacity")

## Time

sec = s
minute = s * 60
min = minute
hour = min * 60
hr = hour
day = hr * 24
d = day
da = day
week = day * 7
wk = week
sennight = day * 7
fortnight = day * 14
blink = day * ten**-5  ## Actual human blink takes 1/3 second
ce = day * ten**-2

## CODATA Physical constants


elementary_charge = plusminus(1.6021766208e-19, 0.0000000098e-19) * C
h = plusminus(6.626070040e-34, 0.000000081e-34) * (J * s)
classical_electron_radius = plusminus(2.8179403227e-15, 0.0000000019e-15) * m
thomson_cross_section = plusminus(0.66524587158e-28, 0.00000000091e-28) * (m**2)
G = plusminus(6.67408e-11, 0.00031e-11) * (N * m**2 / kg**2)
standard_gravity = 9.80662 * m / s**2
atomic_mass_unit = plusminus(1.660539040e-27, 0.000000020e-27) * kg
avogadro = plusminus(6.022140857e23, 0.000000074e23) * (mol**-1)
gas_constant = plusminus(8.3144598, 0.0000048) * (J / (mol * K))
boltzmann = plusminus(1.38064852e-23, 0.00000079e-23) * J/K
wien_displacement = plusminus(2.8977729e-3, 0.0000017e-3)  * (m * K)
electron_mass = plusminus(9.10938356e-31, 0.00000011e-31) * kg
proton_mass = plusminus(1.672621898e-27, 0.000000021e-27) * kg
neutron_mass = plusminus(1.674927471e-27, 0.000000021e-27) * kg
muon_mass = plusminus(1.883531594e-28, 0.000000048e-28) * kg
deuteron_mass = plusminus(3.343583719e-27, 0.000000041e-27) * kg
alpha_particle_mass = plusminus(6.644657230e-27, 0.000000082e-27) * kg
tau_mass = plusminus(3.16747e-27, 0.00029e-27) * kg
alpha = plusminus(7.2973525664e-3, 0.0000000017e-3) 
Rydberg_constant = plusminus(10973731.568508, 0.000065) * (m**-1)
bohr_radius = plusminus(0.52917721067e-10, 0.00000000012e-10) * m
planck_temperature = plusminus(1.416808e32, 0.000033e32) * K
muon_magnetic_moment = plusminus(-4.49044826e-26, 0.00000010e-26) * (J/T)
proton_magnetic_moment = plusminus(1.4106067873e-26, 0.0000000097e-26) * (J/T)
electron_magnetic_moment = plusminus(-928.4764520e-26, 0.0000057e-26) * (J/T)
neutron_magnetic_moment = plusminus(-0.96623650e-26, 0.00000023e-26) * (J/T)
deuteron_magnetic_moment = plusminus(0.4330735040e-26, 0.0000000036e-26) * (J/T)

## DATA

earth_mass = plusminus(5.9722e24, 6.0e20) * kg
earth_radius = plusminus(6371, 10) * kilo * m


year = data(values=[365, 366], weights=[303, 97]) * day    ##  In the gregorian calendar, the calendar cycles every 400 years.
                                                            ## 303 are 365, 97 are leap years with 366 days.
yr = year

month = data(values=[31,29,30,28], weights=[2800, 97, 1600, 303]) * day
                                ##  Using the same math above, in a 400 year cycle the calendar repeats.

