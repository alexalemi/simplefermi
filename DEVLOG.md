# DEVLOG

I'm trying to build a minimalistic implementation of fermi.

## 2022-07-06

Right now I think I have some basic distributions and some dimensions working,
seems like the principle things to work out are the reprs at this point.

One thing to consider is that I could implement `Around` from [wolfram](https://reference.wolfram.com/language/ref/Around.html) which seems to be the base line api that I want.  It handles percent error, relative errors, estimating from a list, etc.
