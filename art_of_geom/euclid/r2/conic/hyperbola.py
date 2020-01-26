__all__ = 'HyperbolaInR2', 'HyperbolaR2', 'Hyperbola'


from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.expr import Expr
from sympy.core.singleton import S

from ..point import PointInR2
from . import ConicInR2


class HyperbolaInR2(ConicInR2):
    def __init__(cls, /, focus: PointInR2, vertex: PointInR2, eccentricity: Expr, *, name: str = None) -> None:
        global_assumptions.add(
            Q.positive(eccentricity - S.One),
            Q.finite(eccentricity))

        super().__init__(
            focus=focus,
            vertex=vertex,
            eccentricity=eccentricity,
            name=name)

    def __repr__(self) -> str:
        return 'Hyperbola {}'.format(self.name)


# aliases
Hyperbola = HyperbolaR2 = HyperbolaInR2
