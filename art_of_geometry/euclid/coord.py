__all__ = 'T', 'U', 'V'


from random import uniform
from sympy.core.symbol import Symbol


# parameters for parametric equations
T = Symbol(name='t', real=True)
U = Symbol(name='t', real=True)
V = Symbol(name='t', real=True)


DEFAULT_INIT_MAX_ABS_COORD = 10


def rand_coord(min_coord, max_coord):
    return uniform(min_coord, max_coord)
