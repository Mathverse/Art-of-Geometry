__all__ = \
    '_EuclidLinearEntityABC', '_EuclidConcreteLinearEntityABC', '_EuclidLinearEntityAtInfinityABC', \
    '_EuclidConcreteLineABC', '_EuclidLineAtInfinityABC', \
    '_EuclidRayABC', '_EuclidSegmentABC'


from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point
from typing import Optional

from ...util.compat import cached_property
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

    def perpendicular_projection_of_point(
            self,
            point: _ConcretePointABC, /,
            *, name: Optional[str] = None) \
            -> _ConcretePointABC:
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
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else '{} *-- {}'.format(
                self.point_0.name,
                self.point_1.name)

    def __repr__(self) -> str:
        return 'Ray {}'.format(self.name)


class _EuclidSegmentABC(_EuclidConcreteLinearEntityABC, Segment):
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else '{} *-* {}'.format(
                self.point_0.name,
                self.point_1.name)

    def __repr__(self) -> str:
        return 'Seg {}'.format(self.name)
