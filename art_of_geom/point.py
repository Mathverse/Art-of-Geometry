__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from functools import cached_property
from sympy.core.expr import Expr
from sympy.geometry.point import Point

from . import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    def __repr__(self) -> str:
        return 'Pt {}'.format(self.name)

    @cached_property
    def distance_from_origin(self) -> Expr:
        raise NotImplementedError


class _ConcretePointABC(_PointABC, Point):
    pass


class _PointAtInfinityABC(_PointABC):
    pass
