__all__ = 'CircleInR2', 'CircleR2', 'Circle'


from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.geometry.ellipse import Circle as SymPyCircle
from sympy.geometry.exceptions import GeometryError
from typing import Tuple

from ....coord import THETA
from ... import _EuclidR2GeometryEntityABC
from ...coord import X, Y
from ...point import PointInR2


class CircleInR2(_EuclidR2GeometryEntityABC):
    def __init__(self, /, center: PointInR2, radius: Symbol, *, name: str = None) -> None:
        assert isinstance(center, PointInR2), \
            GeometryError(
                '*** CENTER {} NOT {} ***'
                .format(center, PointInR2.__name__))

        self.center = center

        self.radius = radius

        self._name = name

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else '{}({})'.format(
                self.center.name,
                self.radius)

    def __repr__(self) -> str:
        return 'Cir {}'.format(self.name)

    @property
    def equation(self) -> Expr:
        return (X - self.center.x) ** 2 \
             + (Y - self.center.y) ** 2 \
             - self.radius ** 2

    @property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        return X - self.center.x - self.radius * cos(THETA), \
               Y - self.center.y - self.radius * sin(THETA)


# aliases
Circle = CircleR2 = CircleInR2
