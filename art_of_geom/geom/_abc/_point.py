__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from sympy.geometry.point import Point

from ...util.compat import cached_property
from ..var import Variable
from ._entity import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @cached_property
    def distance_from_origin(self) -> Variable:
        raise NotImplementedError


class _ConcretePointABC(_PointABC, Point):
    @property
    def free(self) -> bool:
        raise NotImplementedError


class _PointAtInfinityABC(_PointABC):
    pass
