from __future__ import annotations


__all__ = \
    'LineInR3', 'LineR3', 'Line', 'Ln', \
    'LineAtInfinityInR3', 'LineAtInfinityR3', 'LineAtInfinity', 'LineAtInf', 'LnAtInf', \
    'RayInR3', 'RayR3', 'Ray', \
    'SegmentInR3', 'SegmentR3', 'Segment', 'Seg'


from sympy.core.expr import Expr
from sympy.geometry.line import LinearEntity3D, Line3D, Ray3D, Segment3D
from typing import Optional, Tuple

from ...._util._compat import cached_property
from .._abc._coord import T
from .._abc._line import \
    _EuclideanLinearEntityABC, _EuclideanConcreteLinearEntityABC, _EuclideanLinearEntityAtInfinityABC, \
    _EuclideanLineABC, _EuclideanConcreteLineABC, _EuclideanLineAtInfinityABC, \
    _EuclideanRayABC, _EuclideanSegmentABC
from ._abc._entity import _EuclideanGeometryEntityInR3ABC
from .coord import X, Y, Z
from .point import _PointInR3ABC, PointInR3, PointAtInfinityInR3


class _LinearEntityInR3ABC(_EuclideanGeometryEntityInR3ABC, _EuclideanLinearEntityABC):
    pass


class _ConcreteLinearEntityInR3ABC(_LinearEntityInR3ABC, _EuclideanConcreteLinearEntityABC, LinearEntity3D):
    pass


class _LinearEntityAtInfinityInR3ABC(_LinearEntityInR3ABC, _EuclideanLinearEntityAtInfinityABC):
    pass


class _LineInR3ABC(_LinearEntityInR3ABC, _EuclideanLineABC):
    pass


@_LineInR3ABC.assign_name_and_dependencies
class LineInR3(_LineInR3ABC, _EuclideanConcreteLineABC, Line3D):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, /) -> Line3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR3.__name__} ***')

        if isinstance(point_1, PointInR3):
            line = super().__new__(cls, p1=point_0, pt=point_1)

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
            raise TypeError(f'*** POINT_1 {point_1} '
                            f'NEITHER OF TYPE {PointInR3.__name__} '
                            f'NOR OF TYPE {PointAtInfinityInR3.__name__} ***')

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, /) -> None:
        self.point_0 = point_0
        self.point_1 = point_1

    @cached_property
    def point_at_infinity(self) -> PointAtInfinityInR3:
        return self.point_1 \
            if self._point_1_at_infinity \
          else PointAtInfinityInR3(self.direction)

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        return X - self.point_0.x - self.direction.x * T, \
               Y - self.point_0.y - self.direction.y * T, \
               Z - self.point_0.z - self.direction.z * T

    def parallel_line(self, through_euclidean_point: PointInR3, /) -> LineInR3:
        return LineInR3(through_euclidean_point, PointAtInfinityInR3(self.direction))

    def perpendicular_line(self, through_euclidean_point: PointInR3, /) -> LineInR3:
        return LineInR3(through_euclidean_point, self.perpendicular_projection_of_point(through_euclidean_point))
        # TODO: CASE WHEN through_point ON THIS LINE


# aliases
Ln = Line = LineR3 = LineInR3


class LineAtInfinityInR3(_LineInR3ABC, _EuclideanLineAtInfinityABC):
    # TODO
    pass


# aliases
LnAtInf = LineAtInf = LineAtInfinity = LineAtInfinityR3 = LineAtInfinityInR3


class RayInR3(_LinearEntityInR3ABC, _EuclideanRayABC, Ray3D):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, *, name: Optional[str] = None) -> Ray3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR3.__name__} ***')

        if isinstance(point_1, PointInR3):
            ray = super().__new__(cls, p1=point_0, pt=point_1)

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
            raise TypeError(f'*** POINT_1 {point_1} '
                            f'NEITHER OF TYPE {PointInR3.__name__} '
                            f'NOR OF TYPE {PointAtInfinityInR3.__name__} ***')

    def __init__(
            self,
            point_0: PointInR3, point_1: _PointInR3ABC, /,
            *, name: Optional[str] = None) \
            -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR3(self.direction)

        self._name = name


# aliases
Ray = RayR3 = RayInR3


class SegmentInR3(_LinearEntityInR3ABC, _EuclideanSegmentABC, Segment3D):
    def __new__(
            cls,
            point_0: PointInR3, point_1: PointInR3, /,
            *, name: Optional[str] = None) \
            -> Segment3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR3.__name__} ***')

        assert isinstance(point_1, PointInR3), \
            TypeError(f'*** POINT_1 {point_1} NOT OF TYPE {PointInR3.__name__} ***')

        return super().__new__(cls, p1=point_0, p2=point_1)

    def __init__(
            self,
            point_0: PointInR3, point_1: PointInR3, /,
            *, name: Optional[str] = None) \
            -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self._name = name


# aliases
Seg = Segment = SegmentR3 = SegmentInR3
