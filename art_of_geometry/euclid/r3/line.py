__all__ = \
    'LineInR3', 'LineR3', 'Line', 'Ln', \
    'RayInR3', 'RayR3', 'Ray', \
    'SegmentInR3', 'SegmentR3', 'Segment', 'Seg'


from sympy.geometry.line import Line3D, Ray3D, Segment3D
from sympy.geometry.exceptions import GeometryError

from ... import _GeometryEntityABC
from .point import _PointInR3ABC, PointInR3, PointAtInfinityInR3


class LineInR3(Line3D, _GeometryEntityABC):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, name: str = None):
        assert isinstance(point_0, PointInR3), \
            GeometryError(
                '*** POINT_0 {} NOT {} ***'
                    .format(point_0, PointInR3.__name__))

        if isinstance(point_1, PointInR3):
            line = super().__new__(
                cls,
                p1=point_0,
                pt=point_1)

            line._point_1_at_infinity = False

            return line

        elif isinstance(point_1, PointAtInfinityInR3):
            line = super().__new__(
                cls,
                p1=point_0,
                pt=point_0 + point_1.direction)

            line._point_1_at_infinity = True

            return line

        else:
            raise GeometryError(
                '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR3.__name__, PointAtInfinityInR3.__name__))

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, name: str = None):
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR3(direction=self.direction)

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
Ln = Line = LineR3 = LineInR3


class RayInR3(Ray3D, _GeometryEntityABC):
    def __new__(cls, point_0: PointInR3, point_1: _PointInR3ABC, name: str = None):
        assert isinstance(point_0, PointInR3)

        if isinstance(point_1, PointInR3):
            ray = super().__new__(
                cls,
                p1=point_0,
                pt=point_1)

            ray._point_1_at_infinity = False

            return ray

        elif isinstance(point_1, PointAtInfinityInR3):
            ray = super().__new__(
                cls,
                p1=point_0,
                pt=point_0 + point_1.direction)

            ray._point_1_at_infinity = True

            return ray

        else:
            raise TypeError(
                '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR3.__name__, PointAtInfinityInR3.__name__))

    def __init__(self, point_0: PointInR3, point_1: _PointInR3ABC, name: str = None):
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR3(direction=self.direction)

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


# aliases
Ray = RayR3 = RayInR3


class SegmentInR3(Segment3D, _GeometryEntityABC):
    def __new__(cls, point_0: PointInR3, point_1: PointInR3, name: str = None):
        return super().__new__(
            cls,
            p1=point_0, p2=point_1)

    def __init__(self, point_0: PointInR3, point_1: PointInR3, name: str = None):
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


# aliases
Seg = Segment = SegmentR3 = SegmentInR3
