from __future__ import annotations


__all__ = '_EuclideanPointABC', '_EuclideanConcretePointABC', '_EuclideanPointAtInfinityABC'


from abc import abstractmethod
from sympy.core.expr import Expr
from sympy.core.numbers import oo

from ....geom.var import Variable
from ...._util._compat import cached_property
from ...._util._type import print_obj_and_type
from ..._abc._point import _PointABC, _ConcretePointABC, _PointAtInfinityABC


class _EuclideanPointABC(_PointABC):
    @abstractmethod
    def euclidean_distance(self, other_euclidean_point: _EuclideanPointABC, /) -> Variable:
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def euclidean_distance_from_origin(self) -> Variable:
        raise NotImplementedError


class _EuclideanConcretePointABC(_EuclideanPointABC, _ConcretePointABC):
    pass


class _EuclideanPointAtInfinityABC(_EuclideanPointABC, _PointAtInfinityABC):
    def __eq__(self, other_euclidean_point_at_infinity: _EuclideanPointAtInfinityABC, /) -> bool:
        assert isinstance(other_euclidean_point_at_infinity, _type := type(self)), \
            TypeError(f'*** OTHER_EUCLIDEAN_POINT_AT_INFINITY {print_obj_and_type(other_euclidean_point_at_infinity)} '
                      f'NOT OF SAME TYPE {_type.__name__} ***')

        return self.direction.is_scalar_multiple(other_euclidean_point_at_infinity.direction)

    def same(self) -> _EuclideanPointAtInfinityABC:
        return type(self)(self.direction)

    def euclidean_distance(self, other_euclidean_point: _EuclideanPointABC, /) -> Expr:
        raise oo

    @cached_property
    def euclidean_distance_from_origin(self) -> Expr:
        return oo
