__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from sympy.core.expr import Expr
from sympy.geometry.point import Point

from .abc import _GeometryEntityABC
from ..util.compat import cached_property


class _PointABC(_GeometryEntityABC):
    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @cached_property
    def distance_from_origin(self) -> Expr:
        raise NotImplementedError


class _ConcretePointABC(_PointABC, Point):
    pass


class _PointAtInfinityABC(_PointABC):
    pass
