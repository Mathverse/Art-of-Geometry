__all__ = \
    'Point', 'Pt', \
    'ORIGIN_POINT', 'HORIZONTAL_UNIT_POINT', 'VERTICAL_UNIT_POINT',  \
    'PointAtInfinity', 'PtAtInf', 'PointAtInf', \
    'HORIZONTAL_POINT_AT_INFINITY', 'VERTICAL_POINT_AT_INFINITY', 'VERTICAL_POINT_AT_MINUS_INFINITY'


from sympy.core.numbers import Infinity, NegativeInfinity, NegativeOne, One, Pi, Zero, oo, pi
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


# alias
Pt = Point


ORIGIN_POINT = Pt(x=S.Zero, y=S.Zero, name='ORIGIN POINT')

HORIZONTAL_UNIT_POINT = Pt(x=S.One, y=S.Zero, name='HORIZONTAL UNIT POINT')

VERTICAL_UNIT_POINT = Pt(x=S.Zero, y=S.One, name='VERTICAL UNIT POINT')


class PointAtInfinity(_PointABC):
    def __init__(self, slope, name=str(uuid4())):
        self.slope = slope

        self._name = name

    def __repr__(self):
        return 'Pt@Inf {}'.format(self.name)


# aliases
PtAtInf = PointAtInf = PointAtInfinity


HORIZONTAL_POINT_AT_INFINITY = PtAtInf(slope=S.Zero, name='HORIZONTAL_POINT_AT_INFINITY')

VERTICAL_POINT_AT_INFINITY = PtAtInf(slope=oo, name='VERTICAL_POINT_AT_INFINITY')
VERTICAL_POINT_AT_MINUS_INFINITY = PtAtInf(slope=S.NegativeInfinity, name='VERTICAL_POINT_AT_MINUS_INFINITY')
