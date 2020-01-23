__all__ = \
    'LineInR2', 'LineR2', 'Line', 'Ln', \
    'RayInR2', 'RayR2', 'Ray', \
    'SegmentInR2', 'SegmentR2', 'Segment', 'Seg'


from sympy.geometry.line import Line2D, Ray2D, Segment2D
from sympy.geometry.exceptions import GeometryError

from ... import _GeometryEntityABC
from .point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


class LineInR2(Line2D, _GeometryEntityABC):
    def __new__(cls, point_0: PointInR2, point_1: _PointInR2ABC, name: str = None):
        assert isinstance(point_0, PointInR2), \
            GeometryError(
                '*** POINT_0 {} NOT {} ***'
                .format(point_0, PointInR2.__name__))
        
        if isinstance(point_1, PointInR2):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            line._point_1_at_infinity = False

            return line
        
        elif isinstance(point_1, PointAtInfinityInR2):
            line = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            line._point_1_at_infinity = True

            return line
        
        else:
            raise GeometryError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR2.__name__, PointAtInfinityInR2.__name__))

    def __init__(self, point_0: PointInR2, point_1: _PointInR2ABC, name: str = None):
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR2(direction=self.direction)

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
Ln = Line = LineR2 = LineInR2


class RayInR2(Ray2D, _GeometryEntityABC):
    def __new__(cls, point_0: PointInR2, point_1: _PointInR2ABC, name: str = None):
        assert isinstance(point_0, PointInR2)

        if isinstance(point_1, PointInR2):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_1)

            ray._point_1_at_infinity = False

            return ray

        elif isinstance(point_1, PointAtInfinityInR2):
            ray = super().__new__(
                    cls,
                    p1=point_0,
                    pt=point_0 + point_1.direction)

            ray._point_1_at_infinity = True

            return ray

        else:
            raise TypeError(
                    '*** POINT_1 {} NEITHER {} NOR {} ***'
                    .format(point_1, PointInR2.__name__, PointAtInfinityInR2.__name__))

    def __init__(self, point_0: PointInR2, point_1: _PointInR2ABC, name: str = None):
        self.point_0 = point_0

        self.point_1 = point_1

        self.point_at_infinity = \
            point_1 \
            if self._point_1_at_infinity \
            else PointAtInfinityInR2(direction=self.direction)

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
Ray = RayR2 = RayInR2


class SegmentInR2(Segment2D, _GeometryEntityABC):
    def __new__(cls, point_0: PointInR2, point_1: PointInR2, name: str = None):
        return super().__new__(
                cls,
                p1=point_0, p2=point_1)

    def __init__(self, point_0: PointInR2, point_1: PointInR2, name: str = None):
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
Seg = Segment = SegmentR2 = SegmentInR2
