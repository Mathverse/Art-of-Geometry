__all__ = \
    'LineInR2', 'LineR2', 'Line', 'Ln', \
    'LineAtInfinityInR2', 'LineAtInfinityR2', 'LineAtInfinity', 'LineAtInf', 'LnAtInf', \
    'RayInR2', 'RayR2', 'Ray', \
    'SegmentInR2', 'SegmentR2', 'Segment', 'Seg'


from sympy.core.expr import Expr
from sympy.geometry.line import LinearEntity2D, Line2D, Ray2D, Segment2D
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.point import Point2D
from typing import Tuple

from ....util.compat import cached_property
from ..coord import T
from ..line import \
    _EuclidLinearEntityABC, _EuclidConcreteLinearEntityABC, _EuclidLinearEntityAtInfinityABC, \
    _EuclidLineABC, _EuclidConcreteLineABC, _EuclidLineAtInfinityABC, \
    _EuclidRayABC, _EuclidSegmentABC
from .abc import _EuclidGeometryEntityInR2ABC
from .coord import X, Y
from .point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


class _LinearEntityInR2ABC(_EuclidGeometryEntityInR2ABC, _EuclidLinearEntityABC):
    pass


class _ConcreteLinearEntityInR2ABC(_LinearEntityInR2ABC, _EuclidConcreteLinearEntityABC, LinearEntity2D):
    pass


class _LinearEntityAtInfinityInR2ABC(_LinearEntityInR2ABC, _EuclidLinearEntityAtInfinityABC):
    pass


class _LineInR2ABC(_LinearEntityInR2ABC, _EuclidLineABC):
    pass


class LineInR2(_LineInR2ABC, _EuclidConcreteLineABC, Line2D):
    def __new__(cls, point_0: PointInR2, point_1: _PointInR2ABC, *, name: str = None) -> Line2D:
        assert isinstance(point_0, PointInR2), \
            TypeError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR2.__name__))
        
        if isinstance(point_1, PointInR2):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            line._point_1_at_infinity = False

            return line
        
        elif isinstance(point_1, PointAtInfinityInR2):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            line._point_1_at_infinity = True

            return line
        
        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER OF TYPE {} NOR OF TYPE {} ***'
                    .format(point_1, PointInR2.__name__, PointAtInfinityInR2.__name__))

    def __init__(self, point_0: PointInR2, point_1: _PointInR2ABC, *, name: str = None) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR2(self.direction)

        self._name = name

    @cached_property
    def equation(self) -> Expr:
        return self.direction.y * (X - self.point_0.x) \
             - self.direction.x * (Y - self.point_0.y)

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        return X - self.point_0.x - self.direction.x * T, \
               Y - self.point_0.y - self.direction.y * T

    def same(self, *, name=None):
        return LineInR2(
                self.point_0,
                self.point_1,
                name=name)

    def parallel_line(self, through_point: PointInR2, *, name=None):
        return LineInR2(
                through_point,
                PointAtInfinityInR2(self.direction),
                name=name)

    def perpendicular_line(self, through_point: PointInR2, *, name=None):
        return LineInR2(
                through_point,
                PointAtInfinityInR2(self.direction.orthogonal_direction),
                name=name)


# alias
Ln = Line = LineR2 = LineInR2


class LineAtInfinityInR2(_LineInR2ABC, _EuclidLineAtInfinityABC):
    def __init__(self, normal_direction: Point2D, *, name=None) -> None:
        assert isinstance(normal_direction, Point2D), \
            TypeError(
                '*** NORMAL DIRECTION {} NOT OF TYPE {} ***'
                .format(normal_direction, Point2D.__name__))

        self.normal_direction = normal_direction

        self._name = name

    def __eq__(self, line_at_infinity) -> bool:
        assert isinstance(line_at_infinity, LineAtInfinityInR2), \
            TypeError(
                '*** POINT_AT_INFINITY {} NOT OF TYPE {} ***'
                    .format(line_at_infinity, LineAtInfinityInR2.__name__))

        return self.normal_direction.is_scalar_multiple(line_at_infinity.normal_direction)

    def same(self, *, name=None):
        return LineAtInfinityInR2(
                self.normal_direction,
                name=name)

    def parallel_line(self, through_point: PointInR2, *, name=None):
        return LineInR2(
                through_point,
                PointAtInfinityInR2(self.normal_direction.orthogonal_direction),
                name=name)

    def perpendicular_line(self, through_point: PointInR2, *, name=None):
        return LineInR2(
                through_point,
                PointAtInfinityInR2(self.normal_direction),
                name=name)


# aliases
LnAtInf = LineAtInf = LineAtInfinity = LineAtInfinityR2 = LineAtInfinityInR2


class RayInR2(_ConcreteLinearEntityInR2ABC, _EuclidRayABC, Ray2D):
    def __new__(cls, point_0: PointInR2, point_1: _PointInR2ABC, *, name: str = None) -> Ray2D:
        assert isinstance(point_0, PointInR2), \
            TypeError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR2.__name__))

        if isinstance(point_1, PointInR2):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

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
            raise TypeError(
                    '*** POINT_1 {} NEITHER OF TYPE {} NOR OF TYPE {} ***'
                    .format(point_1, PointInR2.__name__, PointAtInfinityInR2.__name__))

    def __init__(self, point_0: PointInR2, point_1: _PointInR2ABC, *, name: str = None) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR2(self.direction)

        self._name = name


# aliases
Ray = RayR2 = RayInR2


class SegmentInR2(_ConcreteLinearEntityInR2ABC, _EuclidSegmentABC, Segment2D):
    def __new__(cls, point_0: PointInR2, point_1: PointInR2, *, name: str = None) -> Segment2D:
        assert isinstance(point_0, PointInR2), \
            TypeError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR2.__name__))

        assert isinstance(point_1, PointInR2), \
            TypeError(
                '*** POINT_1 {} NOT OF TYPE {} ***'
                    .format(point_1, PointInR2.__name__))

        return super().__new__(
                cls,
                p1=point_0,
                p2=point_1)

    def __init__(self, point_0: PointInR2, point_1: PointInR2, *, name: str = None) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self._name = name


# aliases
Seg = Segment = SegmentR2 = SegmentInR2
