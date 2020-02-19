from __future__ import annotations


__all__ = '_PointABC', '_ConcretePointABC', '_PointAtInfinityABC'


from abc import abstractmethod
from sympy.geometry.point import Point

from ._entity import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    _NAME_NULLABLE = False

    # *** ALREADY IMPLEMENTED IN SymPy ***
    # @abstractmethod
    # def __eq__(self, other_point: _PointABC, /) -> bool:
    #     raise NotImplementedError

    def __ne__(self, other_point: _PointABC, /) -> bool:
        return not (self == other_point)


class _ConcretePointABC(_PointABC):   # don't inherit SymPy Point prematurely
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
