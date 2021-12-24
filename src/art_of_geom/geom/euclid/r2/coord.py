__all__ = 'X', 'Y'


from sympy.core.symbol import Symbol

from .._r1.coord import X


# coordinates of real Y axis
Y = Symbol(name='y', real=True)
