__all__ = \
    'Line', 'Ln', \
    'Ray', \
    'Segment', 'Seg'


from sympy.geometry.line import Line2D, Ray2D, Segment2D

from ... import _GeometryEntityABC

from .point import _PointABC, Point, PointAtInfinity


class Line(Line2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: _PointABC):
        return super().__new__(
                    cls,
                    p1=point_0,
                    slope=point_1.slope) \
            if isinstance(point_1, PointAtInfinity) \
          else super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

    def __init__(self, point_0: Point, point_1: _PointABC, name=None):
        self.point_0 = point_0
        self.point_1 = point_1

        self._name = name

    @property
    def name(self):
        return self._name \
            if self._name \
          else '{} --- {}'.format(
                self.point_0.name,
                self.point_1.name)

    def __repr__(self):
        return 'Ln {}'.format(self.name)


# alias
Ln = Line


class Ray(Ray2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: _PointABC):
        return super().__new__(
                cls,
                p1=point_0,
                angle=point_1.slope) \
            if isinstance(point_1, PointAtInfinity) \
          else super().__new__(
                cls,
                p1=point_0,
                pt=point_1)

    def __init__(self, point_0: Point, point_1: _PointABC, name=None):
        self.point_0 = point_0
        self.point_1 = point_1

        self._name = name

    @property
    def name(self):
        return self._name \
            if self._name \
          else '{} *-- {}'.format(
                self.point_0.name,
                self.point_1.name)

    def __repr__(self):
        return 'Ray {}'.format(self.name)


class Segment(Segment2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: Point):
        return super().__new__(
                cls,
                p1=point_0, p2=point_1)

    def __init__(self, point_0: Point, point_1: Point, name=None):
        self.point_0 = point_0
        self.point_1 = point_1

        self._name = name

    @property
    def name(self):
        return self._name \
            if self._name \
          else '{} *-* {}'.format(
                self.point_0.name,
                self.point_1.name)

    def __repr__(self):
        return 'Seg {}'.format(self.name)


# alias
Seg = Segment
