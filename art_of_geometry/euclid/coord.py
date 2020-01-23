__all__ = 'T', 'U', 'V', 'THETA'


from random import uniform
from sympy.core.symbol import Symbol


# parameters for parametric equations
T = Symbol(name='t', real=True)
U = Symbol(name='u', real=True)
V = Symbol(name='v', real=True)
THETA = Symbol(name='θ', real=True)


DEFAULT_INIT_MAX_ABS_COORD = 10


def rand_coord(min_coord, max_coord):
    return uniform(min_coord, max_coord)
