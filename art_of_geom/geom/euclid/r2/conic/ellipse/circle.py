__all__ = 'CircleInR2', 'CircleR2', 'Circle'


from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.expr import Expr
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.geometry.ellipse import Circle as Circle2D
from typing import Optional, Tuple

from ......util.compat import cached_property
from ....coord import THETA
from ...abc import _EuclidGeometryEntityInR2ABC
from ...coord import X, Y
from ...point import PointInR2


class CircleInR2(_EuclidGeometryEntityInR2ABC):
    def __init__(
            self,
            /, center: PointInR2, radius: Expr,
            *, name: Optional[str] = None) \
            -> None:
        assert isinstance(center, PointInR2), \
            TypeError(f'*** CENTER {center} NOT {PointInR2.__name__} ***')

        global_assumptions.add(Q.nonnegative(radius))

        self.center = center

        self.radius = radius

        self._name = name

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.center.name}({self.radius})'

    def __repr__(self) -> str:
        return f'Cir {self.name}'

    @cached_property
    def equation(self) -> Expr:
        return (X - self.center.x) ** 2 \
             + (Y - self.center.y) ** 2 \
             - self.radius ** 2

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        return X - self.center.x - self.radius * cos(THETA), \
               Y - self.center.y - self.radius * sin(THETA)


# aliases
Circle = CircleR2 = CircleInR2
