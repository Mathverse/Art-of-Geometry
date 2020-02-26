from __future__ import annotations


__all__ = \
    '_EuclideanLinearEntityABC', '_EuclideanConcreteLinearEntityABC', '_EuclideanLinearEntityAtInfinityABC', \
    '_EuclideanConcreteLineABC', '_EuclideanConcreteDirectedLineABC', \
    '_EuclideanLineAtInfinityABC', '_EuclideanDirectedLineAtInfinityABC', \
    '_EuclideanRayABC', '_EuclideanSegmentABC'


from abc import abstractmethod
from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point

from ...._util._compat import cached_property
from ....geom._abc._line import \
    _LinearEntityABC, _ConcreteLinearEntityABC, _LinearEntityAtInfinityABC, \
    _LineABC, _ConcreteLineABC, _ConcreteDirectedLineABC, _LineAtInfinityABC, _DirectedLineAtInfinityABC
from ._entity import _EuclideanGeometryEntityABC
from ._point import _EuclideanPointABC, _EuclideanConcretePointABC


class _EuclideanLinearEntityABC(_EuclideanGeometryEntityABC, _LinearEntityABC):
    @abstractmethod
    def parallel_line(self, through_euclidean_point: _EuclideanPointABC, /) -> _EuclideanLineABC:
        raise NotImplementedError

    @abstractmethod
    def perpendicular_projection_of_point(self, euclidean_point: _EuclideanPointABC, /) -> _EuclideanPointABC:
        raise NotImplementedError

    # alias
    def perpendicular_projection(self, euclidean_point: _EuclideanPointABC, /) -> _EuclideanPointABC:
        return self.perpendicular_projection_of_point(euclidean_point)

    @abstractmethod
    def perpendicular_line(self, through_euclidean_point: _EuclideanPointABC, /) -> _EuclideanLineABC:
        raise NotImplementedError


class _EuclideanConcreteLinearEntityABC(_EuclideanLinearEntityABC, _ConcreteLinearEntityABC, LinearEntity):
    @cached_property
    def unit_direction(self) -> Point:
        return self.direction.unit

    def perpendicular_projection_of_point(
            self, euclidean_concrete_point: _EuclideanConcretePointABC, /) \
            -> _EuclideanConcretePointABC:
        return self.point_0 + self.unit_direction.dot(euclidean_concrete_point - self.point_0) * self.unit_direction


class _EuclideanLinearEntityAtInfinityABC(_EuclideanLinearEntityABC, _LinearEntityAtInfinityABC):
    pass


class _EuclideanLineABC(_EuclideanLinearEntityABC, _LineABC):
    pass


class _EuclideanConcreteLineABC(_EuclideanLineABC, _EuclideanConcreteLinearEntityABC, _ConcreteLineABC, Line):
    pass


class _EuclideanConcreteDirectedLineABC(_EuclideanConcreteLineABC, _ConcreteDirectedLineABC):
    pass


class _EuclideanLineAtInfinityABC(_EuclideanLineABC, _EuclideanLinearEntityAtInfinityABC, _LineAtInfinityABC):
    pass


class _EuclideanDirectedLineAtInfinityABC(_EuclideanLineAtInfinityABC, _DirectedLineAtInfinityABC):
    pass


class _EuclideanRayABC(_EuclideanConcreteLinearEntityABC, Ray):
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.point_0.name}->{self.point_1.name}-'

    @property
    def _short_repr(self) -> str:
        return f'Ray {self.name}'


class _EuclideanSegmentABC(_EuclideanConcreteLinearEntityABC, Segment):
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.point_0.name}--{self.point_1.name}'

    @property
    def _short_repr(self) -> str:
        return f'Seg {self.name}'
