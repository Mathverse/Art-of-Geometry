"""Anstract Euclidean Point classes."""


from __future__ import annotations

from abc import abstractmethod
from functools import cached_property
from typing import TYPE_CHECKING

from sympy.core.expr import Expr
from sympy.core.numbers import oo

from g import Var
from g._core import APoint, AConcretePoint, APointAtInf, RealNumOrVar
from g._util.type import obj_and_type_str

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self


__all__: Sequence[LiteralString] = ('AnEuclidPoint',
                                    'AEuclidConcretePoint', 'AnEuclidPointAtInf')  # noqa: E501


class AnEuclidPoint(APoint):
    """Anstract Euclidean Point."""

    @abstractmethod
    def euclid_dist(self: Self, other_euclid_point: AnEuclidPoint, /) -> Var:
        """Distance from another Euclidean point."""
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def euclid_dist_from_orig(self: Self) -> RealNumOrVar:
        """Distance from Origin."""
        raise NotImplementedError


class AEuclidConcretePoint(AnEuclidPoint, AConcretePoint):
    """Anstract Euclidean Concrete Point."""


class AnEuclidPointAtInf(AnEuclidPoint, APointAtInf):
    """Anstract Euclidean Point at Infinity."""

    def __eq__(self, other_euclidean_point_at_infinity: AnEuclidPointAtInf, /) -> bool:
        assert isinstance(other_euclidean_point_at_infinity, _type := type(self)), \
            TypeError(f'*** OTHER_EUCLIDEAN_POINT_AT_INFINITY {obj_and_type_str(other_euclidean_point_at_infinity)} '
                      f'NOT OF SAME TYPE {_type.__name__} ***')

        return self.direction.is_scalar_multiple(other_euclidean_point_at_infinity.direction)

    def same(self) -> AnEuclidPointAtInf:
        return type(self)(self.direction)

    def euclidean_distance(self, other_euclidean_point: AnEuclidPoint, /) -> Expr:
        raise oo

    @cached_property
    def euclidean_distance_from_origin(self) -> Expr:
        return oo
