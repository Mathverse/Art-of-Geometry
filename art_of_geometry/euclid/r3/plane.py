__all__ = \
    'PlaneInR3', 'PlaneR3', 'Plane', 'Pln', \
    'PlaneAtInfinityInR3', 'PlaneAtInfinityR3', 'PlaneAtInfinity', 'PlaneAtInf', 'PlnAtInf'


from functools import cached_property
from sympy.core.expr import Expr
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.plane import Plane as Plane3D
from sympy.geometry.point import Point3D
from typing import Tuple

from ..coord import U, V
from . import _EuclidR3GeometryEntityABC
from .coord import X, Y, Z
from .point import _PointInR3ABC, PointInR3, PointAtInfinityInR3


class _PlaneInR3ABC(_EuclidR3GeometryEntityABC):
    pass


class PlaneInR3(_PlaneInR3ABC, Plane3D):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, point_2: _PointInR3ABC, name: str = None) -> Plane3D:
        assert isinstance(point_0, PointInR3), \
            GeometryError(
                '*** POINT_0 {} NOT OF TYPE {} ***'
                .format(point_0, PointInR3.__name__))

        _point_1_at_infinity = isinstance(point_1, PointAtInfinityInR3)

        if _point_1_at_infinity:
            point_1 = point_0 + point_1.direction

        else:
            assert isinstance(point_1, PointInR3), \
                GeometryError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR3.__name__, PointAtInfinityInR3.__name__))

        _point_2_at_infinity = isinstance(point_2, PointAtInfinityInR3)

        if _point_2_at_infinity:
            point_2 = point_0 + point_2.direction

        else:
            assert isinstance(point_2, PointInR3), \
                GeometryError(
                    '*** POINT_2 {} NEITHER {} NOR {} ***'
                    .format(point_2, PointInR3.__name__, PointAtInfinityInR3.__name__))

        plane = super().__new__(
                    cls,
                    pt=point_0,
                    a=point_1,
                    b=point_2)

        plane._point_1_at_infinity = _point_1_at_infinity
        plane._point_2_at_infinity = _point_2_at_infinity

        return plane

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, point_2: _PointInR3ABC, name: str = None) -> None:
        self.point_0 = point_0
        
        self.point_1 = point_1

        self.direction_1 = \
            point_1.direction \
            if self._point_1_at_infinity \
            else (point_1 - point_0)
        
        self.point_2 = point_2

        self.direction_2 = \
            point_2.direction \
            if self._point_2_at_infinity \
            else (point_2 - point_0)
        
        self._name = name

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else '{} --- {} --- {}'.format(
                self.point_0.name,
                self.point_1.name,
                self.point_2.name)

    def __repr__(self) -> str:
        return 'Pln {}'.format(self.name)

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        return X - self.point_0.x - self.direction_1.x * U - self.direction_2.x * V, \
               Y - self.point_0.y - self.direction_1.y * U - self.direction_2.y * V, \
               Z - self.point_0.z - self.direction_1.z * U - self.direction_2.z * V


# aliases
Pln = Plane = PlaneR3 = PlaneInR3


class PlaneAtInfinityInR3(_PlaneInR3ABC):
    def __init__(self, normal_direction: Point3D) -> None:
        assert isinstance(normal_direction, Point3D), \
            GeometryError(
                '*** NORMAL DIRECTION {} NOT OF TYPE {} ***'
                .format(normal_direction, Point3D.__name__))

        self.normal_direction = normal_direction


# aliases
PlnAtInf = PlaneAtInf = PlaneAtInfinity = PlaneAtInfinityR3 = PlaneAtInfinityInR3
