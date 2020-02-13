__all__ = \
    'LineInR2', 'LineR2', 'Line', 'Ln', \
    'LineAtInfinityInR2', 'LineAtInfinityR2', 'LineAtInfinity', 'LineAtInf', 'LnAtInf', \
    'RayInR2', 'RayR2', 'Ray', \
    'SegmentInR2', 'SegmentR2', 'Segment', 'Seg'


from sympy.core.expr import Expr
from sympy.geometry.line import LinearEntity2D, Line2D, Ray2D, Segment2D
from sympy.geometry.point import Point2D
from typing import Optional, Tuple

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
    @_LineInR2ABC._with_name_assignment
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

    @_LineInR2ABC._with_name_assignment
    def __init__(self, point_0: PointInR2, point_1: _PointInR2ABC, /) -> None:
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
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

    @_LineInR2ABC._with_name_assignment
    def same(self) -> 'LineInR2':
        return LineInR2(self.point_0, self.point_1)

    @_LineInR2ABC._with_name_assignment
    def parallel_line(self, through_point: PointInR2, /) -> 'LineInR2':
        return LineInR2(through_point, PointAtInfinityInR2(self.direction))

    @_LineInR2ABC._with_name_assignment
    def perpendicular_line(self, through_point: PointInR2, /) -> 'LineInR2':
        return LineInR2(through_point, PointAtInfinityInR2(self.direction.orthogonal_direction))


# alias
Ln = Line = LineR2 = LineInR2


class LineAtInfinityInR2(_LineInR2ABC, _EuclidLineAtInfinityABC):
    @_LineInR2ABC._with_name_assignment
    def __init__(self, normal_direction: Point2D, /) -> None:
        assert isinstance(normal_direction, Point2D), \
            TypeError(f'*** NORMAL DIRECTION {normal_direction} NOT OF TYPE {Point2D.__name__} ***')

        self.normal_direction = normal_direction

    def __eq__(self, line_at_infinity: 'LineAtInfinityInR2') -> bool:
        assert isinstance(line_at_infinity, LineAtInfinityInR2), \
            TypeError(f'*** OTHER LINE_AT_INFINITY {line_at_infinity} NOT OF TYPE {LineAtInfinityInR2.__name__} ***')

        return self.normal_direction.is_scalar_multiple(line_at_infinity.normal_direction)

    @_LineInR2ABC._with_name_assignment
    def same(self) -> 'LineAtInfinityInR2':
        return LineAtInfinityInR2(self.normal_direction)

    @_LineInR2ABC._with_name_assignment
    def parallel_line(self, through_point: PointInR2, /) -> LineInR2:
        return LineInR2(through_point, PointAtInfinityInR2(self.normal_direction.orthogonal_direction))

    @_LineInR2ABC._with_name_assignment
    def perpendicular_line(self, through_point: PointInR2, /) -> LineInR2:
        return LineInR2(through_point, PointAtInfinityInR2(self.normal_direction))


# aliases
LnAtInf = LineAtInf = LineAtInfinity = LineAtInfinityR2 = LineAtInfinityInR2


class RayInR2(_ConcreteLinearEntityInR2ABC, _EuclidRayABC, Ray2D):
    @_ConcreteLinearEntityInR2ABC._with_name_assignment
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


class SegmentInR2(_ConcreteLinearEntityInR2ABC, _EuclidSegmentABC, Segment2D):
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
