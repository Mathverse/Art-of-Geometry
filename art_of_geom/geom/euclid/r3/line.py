__all__ = \
    'LineInR3', 'LineR3', 'Line', 'Ln', \
    'LineAtInfinityInR3', 'LineAtInfinityR3', 'LineAtInfinity', 'LineAtInf', 'LnAtInf', \
    'RayInR3', 'RayR3', 'Ray', \
    'SegmentInR3', 'SegmentR3', 'Segment', 'Seg'


from sympy.core.expr import Expr
from sympy.geometry.line import LinearEntity3D, Line3D, Ray3D, Segment3D
from sympy.geometry.exceptions import GeometryError
from typing import Tuple

from ....util import cached_property
from ..coord import T
from ..line import \
    _EuclidLinearEntityABC, _EuclidConcreteLinearEntityABC, _EuclidLinearEntityAtInfinityABC, \
    _EuclidLineABC, _EuclidConcreteLineABC, _EuclidLineAtInfinityABC, \
    _EuclidRayABC, _EuclidSegmentABC
from .abc import _EuclidGeometryEntityInR3ABC
from .coord import X, Y, Z
from .point import _PointInR3ABC, PointInR3, PointAtInfinityInR3


class _LinearEntityInR3ABC(_EuclidGeometryEntityInR3ABC, _EuclidLinearEntityABC):
    pass


class _ConcreteLinearEntityInR3ABC(_LinearEntityInR3ABC, _EuclidConcreteLinearEntityABC, LinearEntity3D):
    pass


class _LinearEntityAtInfinityInR3ABC(_LinearEntityInR3ABC, _EuclidLinearEntityAtInfinityABC):
    pass


class _LineInR3ABC(_LinearEntityInR3ABC, _EuclidLineABC):
    pass


class LineInR3(_LineInR3ABC, _EuclidConcreteLineABC, Line3D):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, *, name: str = None) -> Line3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR3.__name__))

        if isinstance(point_1, PointInR3):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            line._point_1_at_infinity = False

            return line

        elif isinstance(point_1, PointAtInfinityInR3):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            line._point_1_at_infinity = True

            return line

        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR3.__name__, PointAtInfinityInR3.__name__))

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, *, name: str = None) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR3(self.direction)

        self._name = name

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        return X - self.point_0.x - self.direction.x * T, \
               Y - self.point_0.y - self.direction.y * T, \
               Z - self.point_0.z - self.direction.z * T

    def parallel_line(self, through_point: PointInR3, *, name=None):
        return LineInR3(
                through_point,
                PointAtInfinityInR3(self.direction),
                name=name)

    def perpendicular_line(self, through_point: PointInR3, *, name=None):
        # TODO: ASSUME through_point NOT ON THIS LINE

        return LineInR3(
                through_point,
                self.perpendicular_projection(through_point),
                name=name)


# aliases
Ln = Line = LineR3 = LineInR3


class LineAtInfinityInR3(_LineInR3ABC, _EuclidLineAtInfinityABC):
    # TODO
    pass


# aliases
LnAtInf = LineAtInf = LineAtInfinity = LineAtInfinityR3 = LineAtInfinityInR3


class RayInR3(_LinearEntityInR3ABC, _EuclidRayABC, Ray3D):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, *, name: str = None) -> Ray3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR3.__name__))

        if isinstance(point_1, PointInR3):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            ray._point_1_at_infinity = False

            return ray

        elif isinstance(point_1, PointAtInfinityInR3):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            ray._point_1_at_infinity = True

            return ray

        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR3.__name__, PointAtInfinityInR3.__name__))

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, *, name: str = None) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR3(self.direction)

        self._name = name


# aliases
Ray = RayR3 = RayInR3


class SegmentInR3(_LinearEntityInR3ABC, _EuclidSegmentABC, Segment3D):
    def __new__(cls, point_0: PointInR3, point_1: PointInR3, *, name: str = None) -> Segment3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR3.__name__))

        assert isinstance(point_1, PointInR3), \
            TypeError(
                '*** POINT_1 {} NOT OF TYPE {} ***'
                .format(point_1, PointInR3.__name__))

        return super().__new__(
                cls,
                p1=point_0,
                p2=point_1)

    def __init__(self, point_0: PointInR3, point_1: PointInR3, *, name: str = None) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self._name = name


# aliases
Seg = Segment = SegmentR3 = SegmentInR3
