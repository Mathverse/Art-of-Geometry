from sympy.core.symbol import Symbol

from ... import _GeometryEntityABC
from ..r2 import X, Y


# coordinate of imaginary W axis
W = Symbol(name='w', real=True)


class _SurfaceInR2IABC(_GeometryEntityABC):
    pass
