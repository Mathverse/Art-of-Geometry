__all__ = \
    'PlaneInR3', 'PlaneR3', 'Plane', 'Pln', \
    'PlaneAtInfinityInR3', 'PlaneAtInfinityR3', 'PlaneAtInfinity', 'PlaneAtInf', 'PlnAtInf'


from sympy.core.expr import Expr
from sympy.geometry.plane import Plane as Plane3D
from sympy.geometry.point import Point3D
from typing import Tuple

from ...._util._compat import cached_property
from .._abc._coord import U, V
from ._abc._entity import _EuclideanGeometryEntityInR3ABC
from .coord import X, Y, Z
from .line import LineInR3
from .point import _PointInR3ABC, PointInR3, PointAtInfinityInR3


class _PlaneInR3ABC(_EuclideanGeometryEntityInR3ABC):
    pass


class PlaneInR3(_PlaneInR3ABC, Plane3D):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, point_2: _PointInR3ABC, *, name: str = None) -> Plane3D:
        assert isinstance(point_0, PointInR3), \
            TypeError(f'*** POINT_0 {point_0} NOT OF TYPE {PointInR3.__name__} ***')

        _point_1_at_infinity = isinstance(point_1, PointAtInfinityInR3)

        if _point_1_at_infinity:
            point_1 = point_0 + point_1.direction

        else:
            assert isinstance(point_1, PointInR3), \
                TypeError(f'*** POINT_1 {point_1} '
                          f'NEITHER OF TYPE {PointInR3.__name__} '
                          f'NOR OF TYPE {PointAtInfinityInR3.__name__} ***')

        _point_2_at_infinity = isinstance(point_2, PointAtInfinityInR3)

        if _point_2_at_infinity:
            point_2 = point_0 + point_2.direction

        else:
            assert isinstance(point_2, PointInR3), \
                TypeError(f'*** POINT_2 {point_2} '
                          f'NEITHER OF TYPE {PointInR3.__name__} '
                          f'NOR OF TYPE {PointAtInfinityInR3.__name__} ***')

        plane = super().__new__(
                    cls,
                    p1=point_0,
                    a=point_1,
                    b=point_2)

        plane._point_1_at_infinity = _point_1_at_infinity
        plane._point_2_at_infinity = _point_2_at_infinity

        return plane

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, point_2: _PointInR3ABC, *, name: str = None) -> None:
        self.point_0 = point_0
        
        self.point_1 = point_1
        self.line_1 = LineInR3(point_0, point_1)
        self.direction_1 = self.line_1.direction
        
        self.point_2 = point_2
        self.line_2 = LineInR3(point_0, point_2)
        self.direction_2 = self.line_2.direction
        
        self._name = name

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'+{self.point_0.name}++{self.point_1.name}++{self.point_2.name}+'

    def __repr__(self) -> str:
        return 'Pln {}'.format(self.name)

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        return X - self.point_0.x - self.direction_1.x * U - self.direction_2.x * V, \
               Y - self.point_0.y - self.direction_1.y * U - self.direction_2.y * V, \
               Z - self.point_0.z - self.direction_1.z * U - self.direction_2.z * V

    @cached_property
    def normal_direction(self):
        return PointInR3(*self.normal_vector)

    def parallel_plane(self, through_point: PointInR3, *, name=None):
        return PlaneInR3(
                through_point,
                PointAtInfinityInR3(self.direction_1),
                PointAtInfinityInR3(self.direction_2),
                name=name)

    def perpendicular_projection(self, point: PointInR3, *, name=None) -> PointInR3:
        perpendicular_projection_1 = self.line_1.perpendicular_projection_of_point(point)

        perpendicular_projection_2 = self.line_2.perpendicular_projection_of_point(point)

        if perpendicular_projection_1 == perpendicular_projection_2:
            if name:
                perpendicular_projection_1.name = name

            return perpendicular_projection_1

        else:
            return LineInR3(
                    perpendicular_projection_1,
                    perpendicular_projection_2) \
                .perpendicular_projection_of_point(
                    point,
                    name=name)

    def perpendicular_line(self, through_point: PointInR3, *, name=None) -> LineInR3:
        return LineInR3(
                through_point,
                PointAtInfinityInR3(self.normal_direction),
                name=name)


# aliases
Pln = Plane = PlaneR3 = PlaneInR3


class DirectedPlaneInR3(PlaneInR3):
    pass


@_PlaneInR3ABC.assign_name_and_dependencies
class PlaneAtInfinityInR3(_PlaneInR3ABC):
    def __init__(self, normal_direction: Point3D) -> None:
        assert isinstance(normal_direction, Point3D), \
            TypeError(f'*** NORMAL DIRECTION {normal_direction} NOT OF TYPE {Point3D.__name__} ***')

        self.normal_direction = normal_direction


# aliases
PlnAtInf = PlaneAtInf = PlaneAtInfinity = PlaneAtInfinityR3 = PlaneAtInfinityInR3


class DirectedPlaneAtInfinityInR3(PlaneAtInfinityInR3):
    pass
