__all__ = 'T', 'U', 'V', 'THETA'


from random import uniform
from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.numbers import pi
from sympy.core.symbol import Symbol


# parameters for Cartesian coordinate parametric equations
T = Symbol(name='t', real=True)
U = Symbol(name='u', real=True)
V = Symbol(name='v', real=True)


# parameter for R2 polar coordinate parametric equations
THETA = Symbol(name='θ', real=True)

global_assumptions.add(
    Q.positive(THETA + pi),
    Q.nonpositive(THETA - pi))


DEFAULT_INIT_MAX_ABS_COORD = 10


def rand_coord(min_coord, max_coord):
    return uniform(min_coord, max_coord)
