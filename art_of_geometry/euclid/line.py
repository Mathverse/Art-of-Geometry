__all__ = '_EuclidLineABC', '_EuclidRayABC', '_EuclidSegmentABC'


from functools import cached_property
from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point

from ..line import _LinearEntityABC, _LineABC


class _EuclidLinearEntityABC(_LinearEntityABC, LinearEntity):
    @cached_property
    def unit_direction(self) -> Point:
        return self.direction.unit


class _EuclidLineABC(_EuclidLinearEntityABC, _LineABC, Line):
    pass


class _EuclidRayABC(_EuclidLinearEntityABC, Ray):
    pass


class _EuclidSegmentABC(_EuclidLinearEntityABC, Segment):
    pass
