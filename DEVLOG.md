# DEVLOG

I'm trying to build a minimalistic implementation of fermi.

## 2022-07-08

So, I realized today that I could just use one of the myriad of existing unit libraries in python and just sort of add on top of that.  It seems there are lots of options including `astropy.units` which may be the most popular, `unyt` which is a relatively new one and `pint` which has a history and I think does a lot of the things I would want in a unit package.  I'm leaning towards using `pint`.

## 2022-07-06

Right now I think I have some basic distributions and some dimensions working,
seems like the principle things to work out are the reprs at this point.

One thing to consider is that I could implement `Around` from [wolfram](https://reference.wolfram.com/language/ref/Around.html) which seems to be the base line api that I want.  It handles percent error, relative errors, estimating from a list, etc.
