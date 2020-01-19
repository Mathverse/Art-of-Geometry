__all__ = \
    'Line', 'Ln', \
    'Ray', \
    'Segment', 'Seg'


from sympy.geometry.line import Line2D, Ray2D, Segment2D

from ... import _GeometryEntityABC
from .point import _PointABC, Point, PointAtInfinity


class Line(Line2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: _PointABC, name: str = None):
        assert isinstance(point_0, Point)
        
        if isinstance(point_1, Point):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            line._point_1_at_infinity = False

            return line
        
        elif isinstance(point_1, PointAtInfinity):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            line._point_1_at_infinity = True

            return line
        
        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, Point.__name__, PointAtInfinity.__name__))

    def __init__(self, point_0: Point, point_1: _PointABC, name: str = None):
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinity(direction=self.direction)

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

    def line_intersection(self, line):
        return self.point_at_infinity \
            if self.is_parallel(line) \
          else Point._from_sympy_point_2d(
                sympy_point_2d=super().intersection(line)[0])


# alias
Ln = Line


class Ray(Ray2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: _PointABC, name: str = None):
        assert isinstance(point_0, Point)

        if isinstance(point_1, Point):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            ray._point_1_at_infinity = False

            return ray

        elif isinstance(point_1, PointAtInfinity):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            ray._point_1_at_infinity = True

            return ray

        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, Point.__name__, PointAtInfinity.__name__))

    def __init__(self, point_0: Point, point_1: _PointABC, name: str = None):
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
    def __new__(cls, point_0: Point, point_1: Point, name: str = None):
        return super().__new__(
                cls,
                p1=point_0, p2=point_1)

    def __init__(self, point_0: Point, point_1: Point, name: str = None):
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
