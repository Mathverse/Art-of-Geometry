__all__ = 'CircleInR2', 'CircleR2', 'Circle'


from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.expr import Expr
from sympy.core.singleton import S
from sympy.functions.elementary.trigonometric import cos, sin
from typing import Tuple

from ...._util._compat import cached_property
from ...var import Variable
from .._abc._coord import THETA
from ._abc._entity import _EuclideanGeometryEntityInR2ABC
from .coord import X, Y
from .point import PointInR2


@_EuclideanGeometryEntityInR2ABC.assign_name_and_dependencies
class CircleInR2(_EuclideanGeometryEntityInR2ABC):
    def __init__(
            self,
            /, center: PointInR2, radius: Expr,
            *, direction_sign: Variable = Variable(S.One)) \
            -> None:
        assert isinstance(center, PointInR2), \
            TypeError(f'*** CENTER {center} NOT {PointInR2.__name__} ***')

        global_assumptions.add(Q.nonnegative(radius))

        self.center = center

        self.radius = radius

        self.direction_sign = direction_sign

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.center.name}(rad: {self.radius}, dir: {self.direction_sign})'

    def __repr__(self) -> str:
        return f'Cir {self.name}'

    @cached_property
    def equation(self) -> Expr:
        return (X - self.center.x) ** 2 \
             + (Y - self.center.y) ** 2 \
             - self.radius ** 2

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        signed_theta = self.direction_sign * THETA

        return X - self.center.x - self.radius * cos(signed_theta), \
               Y - self.center.y - self.radius * sin(signed_theta)


# aliases
Circle = CircleR2 = CircleInR2
