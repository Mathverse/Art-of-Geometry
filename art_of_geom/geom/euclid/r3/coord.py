__all__ = 'X', 'Y', 'Z'


from sympy.core.symbol import Symbol

from ..r2.coord import X, Y


# coordinate of real Z axis
Z = Symbol(name='z', real=True)
