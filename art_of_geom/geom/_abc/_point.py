__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from abc import abstractmethod
from sympy.geometry.point import Point

from ._entity import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    _NAME_NULLABLE = False


class _ConcretePointABC(_PointABC, Point):
    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @property
    @abstractmethod
    def free(self) -> bool:
        raise NotImplementedError


class _PointAtInfinityABC(_PointABC):
    @property
    def _short_repr(self) -> str:
        return f'Pt@Inf {self.name}'
