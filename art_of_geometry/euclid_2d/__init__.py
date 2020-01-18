from sympy.core.symbol import Symbol

from sympy.geometry.point import Point2D

from sympy.geometry.line import Line2D, Ray2D, Segment2D

from uuid import uuid4

from .. import _GeometryEntityABC


class Point(Point2D, _GeometryEntityABC):
    def __new__(cls, name=None):
        if not name:
            name = str(uuid4())

        point = super().__new__(
                    cls,
                    Symbol(name='{}.x'.format(name), real=True),
                    Symbol(name='{}.y'.format(name), real=True))

        point._name = name

        return point


class Line(Line2D, _GeometryEntityABC):
    def __new__(cls, point_0=Point(), point_1=Point(), name=None):
        line = super().__new__(
                cls,
                p1=point_0,
                pt=point_1)

        line.name = \
            name \
            if name \
            else '{} --- {}'.format(point_0.name, point_1.name)

        return line

    def __init__(self, point_0=Point(), point_1=Point(), name=None):
        self.point_0 = point_0
        self.point_1 = point_1

    def __repr__(self):
        return 'Line {}'.format(self.name)


class Ray(Ray2D, _GeometryEntityABC):
    def __new__(cls, point_0=Point(), point_1=Point(), name=None):
        ray = super().__new__(
                cls,
                p1=point_0,
                pt=point_1)

        ray.name = \
            name \
            if name \
            else '{} *-> {}'.format(point_0.name, point_1.name)

        return ray

    def __init__(self, point_0=Point(), point_1=Point(), name=None):
        self.point_0 = point_0
        self.point_1 = point_1

    def __repr__(self):
        return 'Ray {}'.format(self.name)


class Segment(Segment2D, _GeometryEntityABC):
    def __new__(cls, point_0=Point(), point_1=Point(), name=None):
        segment = super().__new__(
                    cls,
                    p1=point_0,
                    p2=point_1)

        segment.name = \
            name \
            if name \
            else '{} *-* {}'.format(point_0.name, point_1.name)

        return segment

    def __init__(self, point_0=Point(), point_1=Point(), name=None):
        self.point_0 = point_0
        self.point_1 = point_1

    def __repr__(self):
        return 'Segment {}'.format(self.name)


class Angle(_GeometryEntityABC):
    def __init__(self, point_0=Point(), point_1=Point(), point_2=Point(), name=None):
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2

    def __repr__(self):
        return 'Angle {}'.format(self.name)
