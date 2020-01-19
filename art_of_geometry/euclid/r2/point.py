__all__ = \
    'Point', 'Pt', \
    'ORIGIN_POINT', 'HORIZONTAL_UNIT_POINT', 'VERTICAL_UNIT_POINT', \
    'PointAtUndirectedInfinity', 'PtAtUndirInf', \
    'POINT_AT_HORIZONTAL_INFINITY', 'POINT_AT_VERTICAL_INFINITY', \
    'PointAtDirectedInfinity', 'PtAtDirInf', \
    'POINT_AT_EAST_INFINITY', 'POINT_AT_WEST_INFINITY', 'POINT_AT_NORTH_INFINITY', 'POINT_AT_SOUTH_INFINITY'


from sympy.core.numbers import Infinity, NegativeInfinity, NegativeOne, One, Pi, Zero, oo, pi, zoo
from sympy.core.singleton import S, Singleton, SingletonRegistry
from sympy.core.symbol import Symbol

from sympy.geometry.point import Point2D

from uuid import uuid4

from ... import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    pass


class Point(Point2D, _PointABC):
    def __new__(cls, x=None, y=None, name=None):
        if not name:
            name = str(uuid4())

        if x is None:
            x = Symbol(name='{}.x'.format(name), real=True)

        if y is None:
            y = Symbol(name='{}.y'.format(name), real=True)

        point = super().__new__(cls, x, y)

        point._name = name

        return point

    def __repr__(self):
        return 'Pt {}'.format(self.name)

    @classmethod
    def _from_sympy_point_2d(cls, sympy_point_2d, name=None):
        return Point(
                x=sympy_point_2d.x,
                y=sympy_point_2d.y,
                name=name)


# alias
Pt = Point

# constants
ORIGIN_POINT = Pt(x=S.Zero, y=S.Zero, name='ORIGIN_POINT')
HORIZONTAL_UNIT_POINT = Pt(x=S.One, y=S.Zero, name='HORIZONTAL_UNIT_POINT')
VERTICAL_UNIT_POINT = Pt(x=S.Zero, y=S.One, name='VERTICAL_UNIT_POINT')


class PointAtUndirectedInfinity(_PointABC):
    def __init__(self, slope, name=None):
        self.slope = slope

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self):
        return 'Pt@UndirInf {}'.format(self.name)

    def __eq__(self, point_at_undirected_infinity):
        assert isinstance(point_at_undirected_infinity, PointAtUndirectedInfinity)

        return self.slope == point_at_undirected_infinity.slope


# alias
PtAtUndirInf = PointAtUndirectedInfinity

# constants
POINT_AT_HORIZONTAL_INFINITY = PtAtUndirInf(slope=S.Zero, name='POINT_AT_HORIZONTAL_INFINITY')
POINT_AT_VERTICAL_INFINITY = PtAtUndirInf(slope=oo, name='POINT_AT_VERTICAL_INFINITY')


class PointAtDirectedInfinity(_PointABC):
    def __init__(self, directed_angle_measure, name=None):
        self.directed_angle_measure = directed_angle_measure

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self):
        return 'Pt@DirInf {}'.format(self.name)

    def __eq__(self, point_at_directed_infinity):
        assert isinstance(point_at_directed_infinity, PointAtDirectedInfinity)

        return self.directed_angle_measure == point_at_directed_infinity.directed_angle_measure


# alias
PtAtDirInf = PointAtDirectedInfinity

# constants
POINT_AT_EAST_INFINITY = PtAtDirInf(directed_angle_measure=S.Zero, name='POINT_AT_EAST_INFINITY')
POINT_AT_WEST_INFINITY = PtAtDirInf(directed_angle_measure=pi, name='POINT_AT_WEST_INFINITY')
POINT_AT_NORTH_INFINITY = PtAtDirInf(directed_angle_measure=pi/2, name='POINT_AT_NORTH_INFINITY')
POINT_AT_SOUTH_INFINITY = PtAtDirInf(directed_angle_measure=-pi/2, name='POINT_AT_NORTH_INFINITY')
