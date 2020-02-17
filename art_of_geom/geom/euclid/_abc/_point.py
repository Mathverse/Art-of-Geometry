from __future__ import annotations


__all__ = '_EuclidPointABC', '_EuclidConcretePointABC', '_EuclidPointAtInfinityABC'


from sympy.core.numbers import oo

from ....geom.var import Variable
from ...._util._compat import cached_property
from ...._util._type import print_obj_and_type
from ..._abc._point import _PointABC, _ConcretePointABC, _PointAtInfinityABC


class _EuclidPointABC(_PointABC):
    pass


class _EuclidConcretePointABC(_EuclidPointABC, _ConcretePointABC):
    pass


class _EuclidPointAtInfinityABC(_EuclidPointABC, _PointAtInfinityABC):
    def __eq__(self, point_at_infinity: _EuclidPointAtInfinityABC, /) -> bool:
        assert isinstance(point_at_infinity, _type := type(self)), \
            TypeError(f'*** OTHER POINT_AT_INFINITY {print_obj_and_type(point_at_infinity)} '
                      f'NOT OF SAME TYPE {_type.__name__} ***')

        return self.direction.is_scalar_multiple(point_at_infinity.direction)

    @_EuclidPointABC._with_dependency_tracking
    @_EuclidPointABC._with_name_assignment
    def same(self) -> _EuclidPointAtInfinityABC:
        return type(self)(self.direction)

    @cached_property
    @_EuclidPointABC._with_dependency_tracking
    def distance_from_origin(self) -> Variable:
        return oo
