from sympy.core.numbers import I
from sympy.core.symbol import Symbol

from ..r2.coord import X, Y


# coordinate of imaginary W axis
W = Symbol(name='w', real=True)

# corresponding complex coordinate
_Z = Y + I * W
