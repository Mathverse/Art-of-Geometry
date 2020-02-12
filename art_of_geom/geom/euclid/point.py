__all__ = '_EuclidPointABC', '_EuclidConcretePointABC', '_EuclidPointAtInfinityABC'


from sympy.core.expr import Expr
from sympy.core.numbers import oo
from typing import Optional

from ...util.compat import cached_property
from ..point import _PointABC, _ConcretePointABC, _PointAtInfinityABC


class _EuclidPointABC(_PointABC):
    pass


class _EuclidConcretePointABC(_EuclidPointABC, _ConcretePointABC):
    pass


class _EuclidPointAtInfinityABC(_EuclidPointABC, _PointAtInfinityABC):
    def __repr__(self) -> str:
        return 'Pt@Inf {}'.format(self.name)

    def __eq__(self, point_at_infinity: _PointAtInfinityABC) -> bool:
        _type = type(self)

        assert isinstance(point_at_infinity, _type), \
            TypeError(f'*** OTHER POINT_AT_INFINITY {point_at_infinity} NOT OF SAME TYPE {_type.__name__} ***')

        return self.direction.is_scalar_multiple(point_at_infinity.direction)

    def same(self, /, *, name: Optional[str] = None):
        return type(self)(
                self.direction,
                name=name)

    @cached_property
    def distance_from_origin(self) -> Expr:
        return oo
