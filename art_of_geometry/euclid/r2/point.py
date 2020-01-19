from sympy.core.symbol import Symbol

from sympy.geometry.point import Point2D

from uuid import uuid4

from ... import _GeometryEntityABC


class Point(Point2D, _GeometryEntityABC):
    def __new__(cls, name=str(uuid4())):
        point = super().__new__(
                    cls,
                    Symbol(name='{}.x'.format(name), real=True),
                    Symbol(name='{}.y'.format(name), real=True))

        point._name = name

        return point

    def __repr__(self):
        return 'Pt {}'.format(self.name)


# alias
Pt = Point


class PointAtInfinity(_GeometryEntityABC):
    def __init__(self, slope, name=str(uuid4())):
        self.slope = slope

        self._name = name

    def __repr__(self):
        return 'Pt@Inf {}'.format(self.name)


# aliases
PtAtInf = PointAtInf = PointAtInfinity
