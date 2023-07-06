# DEVLOG

I'm trying to build a minimalistic implementation of fermi.

## 2023-07-06

Worked on finishing out the library.  I rediscovered that it was reasonably
useful in ipython in the terminal.  I worked on trying to improve the notebook
support by adding a `_repr_html_` which prints the dotplot.  I also added unit
support to the distributions and removed some of the heavy dependencies.

## 2022-07-08

So, I realized today that I could just use one of the myriad of existing unit
libraries in python and just sort of add on top of that.  It seems there are
lots of options including `astropy.units` which may be the most popular, `unyt`
which is a relatively new one and `pint` which has a history and I think does a
lot of the things I would want in a unit package.  I'm leaning towards using
`pint`.  Though one thing to consider is that it seems as though
`astropy.units` is on the default installation path for colab.

So, I switched things over to use `pint` and also tried to redefine the units
to be consistent with the redefinition of SI in 2019.  I also populated the
library namespace with a bunch of things from `pint` as well as the constants
in `astropy.constants`.  I also created a `__main__` module that fills the
default namespace of an ipython session so we can use this as a binary.

## 2022-07-06

Right now I think I have some basic distributions and some dimensions working,
seems like the principle things to work out are the reprs at this point.

One thing to consider is that I could implement `Around` from [wolfram](https://reference.wolfram.com/language/ref/Around.html) which seems to be the base line api that I want.  It handles percent error, relative errors, estimating from a list, etc.
