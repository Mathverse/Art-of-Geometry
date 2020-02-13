__all__ = \
    '_EuclidLinearEntityABC', '_EuclidConcreteLinearEntityABC', '_EuclidLinearEntityAtInfinityABC', \
    '_EuclidConcreteLineABC', '_EuclidLineAtInfinityABC', \
    '_EuclidRayABC', '_EuclidSegmentABC'


from sympy.geometry.line import LinearEntity, Line, Ray, Segment
from sympy.geometry.point import Point

from ...util.compat import cached_property
from ..line import \
    _LinearEntityABC, _ConcreteLinearEntityABC, _LinearEntityAtInfinityABC, \
    _LineABC, _ConcreteLineABC, _ConcreteDirectedLineABC, _LineAtInfinityABC, _DirectedLineAtInfinityABC
from ..point import _ConcretePointABC


class _EuclidLinearEntityABC(_LinearEntityABC):
    pass


class _EuclidConcreteLinearEntityABC(_EuclidLinearEntityABC, _ConcreteLinearEntityABC, LinearEntity):
    @cached_property
    def unit_direction(self) -> Point:
        return self.direction.unit

    @_EuclidLinearEntityABC._with_name_assignment
    def perpendicular_projection_of_point(self, point: _ConcretePointABC, /) -> _ConcretePointABC:
        return self.point_0 + self.unit_direction.dot(point - self.point_0) * self.unit_direction


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
          else f'{self.point_0.name}--{self.point_1.name}-'

    @property
    def _short_repr(self) -> str:
        return f'Ray {self.name}'


class _EuclidSegmentABC(_EuclidConcreteLinearEntityABC, Segment):
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.point_0.name}--{self.point_1.name}'

    @property
    def _short_repr(self) -> str:
        return f'Seg {self.name}'
