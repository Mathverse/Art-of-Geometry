__all__ = \
    'Line', 'Ln', \
    'Ray', \
    'Segment', 'Seg', \
    'Vector', 'Vec'


from sympy.geometry.line import Line2D, Ray2D, Segment2D

from ... import _GeometryEntityABC

from .angle_measure import ray_directed_angle_measure
from .point import _PointABC, Point, PointAtUndirectedInfinity, PointAtDirectedInfinity


class Line(Line2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: _PointABC, name=None):
        assert isinstance(point_0, Point)
        
        if isinstance(point_1, Point):
            line = super().__new__(
                        cls,
                        p1=point_0,
                        pt=point_1)

            line._point_1_at_undirected_infinity = False
        
        elif isinstance(point_1, PointAtUndirectedInfinity):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    slope=point_1.slope)

            line._point_1_at_undirected_infinity = True
        
        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, Point.__name__, PointAtUndirectedInfinity.__name__))

    def __init__(self, point_0: Point, point_1: _PointABC, name=None):
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_undirected_infinity = \
            point_1 \
            if self._point_1_at_undirected_infinity \
            else PointAtUndirectedInfinity(slope=self.slope)

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
        return self.point_at_undirected_infinity \
            if self.is_parallel(line) \
          else Point._from_sympy_point_2d(
                sympy_point_2d=super().intersection(line)[0])


# alias
Ln = Line


class Ray(Ray2D, _GeometryEntityABC):
    def __new__(cls, point_0: Point, point_1: _PointABC, name=None):
        assert isinstance(point_0, Point)

        if isinstance(point_1, Point):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            ray._point_1_at_directed_infinity = False

        elif isinstance(point_1, PointAtDirectedInfinity):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    angle=point_1.directed_angle_measure)

            ray._point_1_at_directed_infinity = True

        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, Point.__name__, PointAtDirectedInfinity.__name__))

    def __init__(self, point_0: Point, point_1: _PointABC, name=None):
        self.point_0 = point_0

        self.point_1 = point_1

        if self._point_1_at_directed_infinity:
            self.point_at_directed_infinity = point_1
            
            self.directed_angle_measure = point_1.directed_angle_measure
            
        else:
            self.directed_angle_measure = \
                ray_directed_angle_measure(
                    point_0=point_0,
                    point_1=point_1)
            
            self.point_at_directed_infinity = \
                PointAtDirectedInfinity(
                    directed_angle_measure=self.directed_angle_measure)

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
    def __new__(cls, point_0: Point, point_1: Point, name=None):
        return super().__new__(
                cls,
                p1=point_0, p2=point_1)

    def __init__(self, point_0: Point, point_1: Point, name=None):
        self.point_0 = point_0
        self.point_1 = point_1

        self.directed_angle_measure = \
            ray_directed_angle_measure(
                point_0=point_0,
                point_1=point_1)

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


class Vector(_GeometryEntityABC):
    @property
    def name(self):
        return self._name \
            if self._name \
          else '{} *-> {}'.format(
                self.point_0.name,
                self.point_1.name)

    def __repr__(self):
        return 'Vec {}'.format(self.name)


# alias
Vec = Vector

