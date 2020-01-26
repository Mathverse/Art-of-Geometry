__all__ = '_EuclidLineABC', '_EuclidRayABC', '_EuclidSegmentABC'


from functools import cached_property
from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point

from ..line import _LinearEntityABC, _LineABC


class _EuclidLinearEntityABC(_LinearEntityABC):   # too early to inherit LinearEntity
    @cached_property
    def unit_direction(self) -> Point:
        return self.direction.unit

    def perpendicular_projection(self, point: Point, /, *, name=None) -> Point:
        projection = \
            self.point_0 + \
            self.unit_direction.dot(point - self.point_0) * self.unit_direction

        if name:
            projection.name = name

        return projection


class _EuclidLineABC(_EuclidLinearEntityABC, _LineABC):   # too early to inherit Line
    pass


class _EuclidRayABC(_EuclidLinearEntityABC, Ray):
    pass


class _EuclidSegmentABC(_EuclidLinearEntityABC, Segment):
    pass
