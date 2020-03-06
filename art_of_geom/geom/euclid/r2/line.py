from __future__ import annotations


__all__ = \
    'LineInR2', 'LineR2', 'Line', 'Ln', \
    'LineAtInfinityInR2', 'LineAtInfinityR2', 'LineAtInfinity', 'LineAtInf', 'LnAtInf', \
    'RayInR2', 'RayR2', 'Ray', \
    'SegmentInR2', 'SegmentR2', 'Segment', 'Seg'


from sympy.core.expr import Expr
from sympy.geometry.line import LinearEntity2D, Line2D, Ray2D, Segment2D
from sympy.geometry.point import Point2D
from typing import Optional, Tuple

from ...._util._compat import cached_property
from .._abc._coord import T
from .._abc._line import \
    _EuclideanLinearEntityABC, _EuclideanConcreteLinearEntityABC, _EuclideanLinearEntityAtInfinityABC, \
    _EuclideanLineABC, _EuclideanConcreteLineABC, _EuclideanLineAtInfinityABC, \
    _EuclideanRayABC, _EuclideanSegmentABC
from ._abc._entity import _EuclideanGeometryEntityInR2ABC
from .coord import X, Y
from .point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


class _LinearEntityInR2ABC(_EuclideanGeometryEntityInR2ABC, _EuclideanLinearEntityABC):
    pass


class _ConcreteLinearEntityInR2ABC(_LinearEntityInR2ABC, _EuclideanConcreteLinearEntityABC, LinearEntity2D):
    pass


class _LinearEntityAtInfinityInR2ABC(_LinearEntityInR2ABC, _EuclideanLinearEntityAtInfinityABC):
    pass


class _LineInR2ABC(_LinearEntityInR2ABC, _EuclideanLineABC):
    pass


@_LineInR2ABC.assign_name_and_dependencies
class LineInR2(_LineInR2ABC, _EuclideanConcreteLineABC, Line2D):
    def __new__(cls, point_0: PointInR2, point_1: _PointInR2ABC, /) -> Line2D:
        assert isinstance(point_0, PointInR2), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR2.__name__} ***')
        
        if isinstance(point_1, PointInR2):
            line = super().__new__(cls, p1=point_0, pt=point_1)

            line._point_1_at_infinity = False

            return line
        
        elif isinstance(point_1, PointAtInfinityInR2):
            line = super().__new__(cls, p1=point_0, pt=point_0 + point_1.direction)

            line._point_1_at_infinity = True

            return line
        
        else:
            raise TypeError(f'*** POINT_1 {point_1} '
                            f'NEITHER OF TYPE {PointInR2.__name__} '
                            f'NOR OF TYPE {PointAtInfinityInR2.__name__} ***')

    def __init__(self, point_0: PointInR2, point_1: _PointInR2ABC, /) -> None:
        self.point_0 = point_0
        self.point_1 = point_1

    @cached_property
    def point_at_infinity(self) -> PointAtInfinityInR2:
        return self.point_1 \
            if self._point_1_at_infinity \
          else PointAtInfinityInR2(self.direction)

    @cached_property
    def equation(self) -> Expr:
        return self.direction.y * (X - self.point_0.x) \
             - self.direction.x * (Y - self.point_0.y)

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        return X - self.point_0.x - self.direction.x * T, \
               Y - self.point_0.y - self.direction.y * T

    def same(self) -> LineInR2:
        return LineInR2(self.point_0, self.point_1)

    def parallel_line(self, through_euclidean_point: PointInR2, /) -> LineInR2:
        return LineInR2(through_euclidean_point, PointAtInfinityInR2(self.direction))

    def perpendicular_line(self, through_euclidean_point: PointInR2, /) -> LineInR2:
        return LineInR2(through_euclidean_point, PointAtInfinityInR2(self.direction.orthogonal_direction))


# alias
Ln = Line = LineR2 = LineInR2


@_LineInR2ABC.assign_name_and_dependencies
class LineAtInfinityInR2(_LineInR2ABC, _EuclideanLineAtInfinityABC):
    def __init__(self, normal_direction: Point2D, /) -> None:
        assert isinstance(normal_direction, Point2D), \
            TypeError(f'*** NORMAL DIRECTION {normal_direction} NOT OF TYPE {Point2D.__name__} ***')

        self.normal_direction = normal_direction

    def __eq__(self, line_at_infinity: LineAtInfinityInR2) -> bool:
        assert isinstance(line_at_infinity, LineAtInfinityInR2), \
            TypeError(f'*** OTHER LINE_AT_INFINITY {line_at_infinity} NOT OF TYPE {LineAtInfinityInR2.__name__} ***')

        return self.normal_direction.is_scalar_multiple(line_at_infinity.normal_direction)

    def same(self) -> LineAtInfinityInR2:
        return LineAtInfinityInR2(self.normal_direction)

    def parallel_line(self, through_euclidean_point: PointInR2, /) -> LineInR2:
        return LineInR2(through_euclidean_point, PointAtInfinityInR2(self.normal_direction.orthogonal_direction))

    def perpendicular_line(self, through_euclidean_point: PointInR2, /) -> LineInR2:
        return LineInR2(through_euclidean_point, PointAtInfinityInR2(self.normal_direction))


# aliases
LnAtInf = LineAtInf = LineAtInfinity = LineAtInfinityR2 = LineAtInfinityInR2


@_ConcreteLinearEntityInR2ABC.assign_name_and_dependencies
class RayInR2(_ConcreteLinearEntityInR2ABC, _EuclideanRayABC, Ray2D):
    def __new__(cls, point_0: PointInR2, point_1: _PointInR2ABC, /) -> Ray2D:
        assert isinstance(point_0, PointInR2), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR2.__name__} ***')

        if isinstance(point_1, PointInR2):
            ray = super().__new__(cls, p1=point_0, pt=point_1)

            ray._point_1_at_infinity = False

            return ray

        elif isinstance(point_1, PointAtInfinityInR2):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            ray._point_1_at_infinity = True

            return ray

        else:
            raise TypeError(f'*** POINT_1 {point_1} '
                            f'NEITHER OF TYPE {PointInR2.__name__} '
                            f'NOR OF TYPE {PointAtInfinityInR2.__name__} ***')

    def __init__(
            self,
            point_0: PointInR2, point_1: _PointInR2ABC, /,
            *, name: Optional[str] = None) \
            -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR2(self.direction)

        self._name = name


# aliases
Ray = RayR2 = RayInR2


@_ConcreteLinearEntityInR2ABC.assign_name_and_dependencies
class SegmentInR2(_ConcreteLinearEntityInR2ABC, _EuclideanSegmentABC, Segment2D):
    def __new__(
            cls,
            point_0: PointInR2, point_1: PointInR2, /,
            *, name: Optional[str] = None) \
            -> Segment2D:
        assert isinstance(point_0, PointInR2), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR2.__name__} ***')

        assert isinstance(point_1, PointInR2), \
            TypeError(f'*** POINT_1 {point_1} NOT OF TYPE {PointInR2.__name__} ***')

        return super().__new__(cls, p1=point_0, p2=point_1)

    def __init__(
            self,
            point_0: PointInR2, point_1: PointInR2, /,
            *, name: Optional[str] = None) \
            -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self._name = name


# aliases
Seg = Segment = SegmentR2 = SegmentInR2
