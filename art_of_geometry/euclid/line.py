__all__ = \
    '_EuclidConcreteLineABC', '_EuclidLineAtInfinityABC', \
    '_EuclidRayABC', '_EuclidSegmentABC'


from functools import cached_property
from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point

from ..line import \
    _LinearEntityABC, _ConcreteLinearEntityABC, _LinearEntityAtInfinityABC, \
    _LineABC, _ConcreteLineABC, _LineAtInfinityABC
from ..point import _ConcretePointABC


class _EuclidLinearEntityABC(_LinearEntityABC):
    pass


class _EuclidConcreteLinearEntityABC(_EuclidLinearEntityABC, _ConcreteLinearEntityABC, LinearEntity):
    @cached_property
    def unit_direction(self) -> Point:
        return self.direction.unit

    def perpendicular_projection(self, point: _ConcretePointABC, /, *, name=None) -> _ConcretePointABC:
        projection = \
            self.point_0 + \
            self.unit_direction.dot(point - self.point_0) * self.unit_direction

        if name:
            projection.name = name

        return projection


class _EuclidLinearEntityAtInfinityABC(_EuclidLinearEntityABC, _LinearEntityAtInfinityABC):
    pass


class _EuclidLineABC(_EuclidLinearEntityABC, _LineABC):
    pass


class _EuclidConcreteLineABC(_EuclidLineABC, _EuclidConcreteLinearEntityABC, _ConcreteLineABC, Line):
    pass


class _EuclidLineAtInfinityABC(_EuclidLineABC, _EuclidLinearEntityAtInfinityABC, _LineAtInfinityABC):
    pass


class _EuclidRayABC(_EuclidConcreteLinearEntityABC, Ray):
    pass


class _EuclidSegmentABC(_EuclidConcreteLinearEntityABC, Segment):
    pass
