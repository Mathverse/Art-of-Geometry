__all__ = '_LineABC'


from abc import abstractmethod
from functools import cached_property
from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point

from . import _GeometryEntityABC
from .point import _PointABC


class _LinearEntityABC(_GeometryEntityABC, LinearEntity):
    @cached_property
    def unit_direction(self) -> Point:
        return self.direction.unit

    @abstractmethod
    def parallel_line(self, through_point: _PointABC, /, *, name=None):
        raise NotImplementedError

    @abstractmethod
    def perpendicular_projection(self, point: _PointABC, /, *, name=None) -> _PointABC:
        raise NotImplementedError

    @abstractmethod
    def perpendicular_line(self, through_point: _PointABC, /, *, name=None):
        raise NotImplementedError


class _LineABC(_LinearEntityABC, Line):
    @abstractmethod
    def perspective_projection(self, /, perspector: _PointABC, point: _PointABC, *, name=None) -> _PointABC:
        raise NotImplementedError


class _RayABC(_LinearEntityABC, Ray):
    pass


class _SegmentABC(_LinearEntityABC, Segment):
    pass
