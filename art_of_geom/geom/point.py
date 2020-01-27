__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from sympy.core.expr import Expr
from sympy.geometry.point import Point

from .abc import _GeometryEntityABC
from ..util import cached_property


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
