__all__ = '_EuclidPointABC', '_EuclidConcretePointABC', '_EuclidPointAtInfinityABC'


from sympy.core.expr import Expr
from sympy.core.numbers import oo

from ...util.compat import cached_property
from ..point import _PointABC, _ConcretePointABC, _PointAtInfinityABC


class _EuclidPointABC(_PointABC):
    pass


class _EuclidConcretePointABC(_EuclidPointABC, _ConcretePointABC):
    pass


class _EuclidPointAtInfinityABC(_EuclidPointABC, _PointAtInfinityABC):
    @property
    def _short_repr(self) -> str:
        return f'Pt@Inf {self.name}'

    def __eq__(self, point_at_infinity: '_EuclidPointAtInfinityABC') -> bool:
        assert isinstance(point_at_infinity, _type := type(self)), \
            TypeError(f'*** OTHER POINT_AT_INFINITY {point_at_infinity} NOT OF SAME TYPE {_type.__name__} ***')

        return self.direction.is_scalar_multiple(point_at_infinity.direction)

    @_EuclidPointABC._with_name_assignment
    def same(self):
        return type(self)(self.direction)

    @cached_property
    def distance_from_origin(self) -> Expr:
        return oo
