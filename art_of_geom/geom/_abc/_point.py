__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from sympy.geometry.point import Point

from ...util.compat import cached_property
from ..var import Variable
from ._entity import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    @cached_property
    @_GeometryEntityABC._with_dependency_tracking
    def distance_from_origin(self) -> Variable:
        raise NotImplementedError


class _ConcretePointABC(_PointABC, Point):
    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @property
    def free(self) -> bool:
        raise NotImplementedError


class _PointAtInfinityABC(_PointABC):
    @property
    def _short_repr(self) -> str:
        return f'Pt@Inf {self.name}'
