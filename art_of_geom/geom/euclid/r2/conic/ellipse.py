__all__ = 'EllipseInR2', 'EllipseR2', 'Ellipse'


from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.expr import Expr
from sympy.core.singleton import S
from sympy.geometry.ellipse import Ellipse as Ellipse2D
from typing import Optional

from ..point import PointInR2
from . import ConicInR2


class EllipseInR2(ConicInR2):
    def __init__(
            cls,
            /, focus: PointInR2, vertex: PointInR2, eccentricity: Expr,
            *, name: str = None) \
            -> None:
        global_assumptions.add(Q.negative(eccentricity - S.One))

        super().__init__(
            focus=focus,
            vertex=vertex,
            eccentricity=eccentricity,
            name=name)

    def __repr__(self) -> str:
        return 'Ellipse {}'.format(self.name)


# aliases
Ellipse = EllipseR2 = EllipseInR2
