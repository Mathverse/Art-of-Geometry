__all__ = \
    'Point', 'Pt', \
    'PointAtInfinity', 'PtAtInf'


from sympy.core.symbol import Symbol

from sympy.geometry.point import Point2D

from uuid import uuid4

from ... import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    pass


class Point(Point2D, _PointABC):
    def __new__(cls, x: Symbol = None, y: Symbol = None, name: str = None):
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
    def _from_sympy_point_2d(cls, sympy_point_2d: Point2D, name: str = None):
        return Point(
                x=sympy_point_2d.x,
                y=sympy_point_2d.y,
                name=name)


# alias
Pt = Point


class PointAtInfinity(_PointABC):
    def __init__(self, direction: Point, name: str = None):
        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self):
        return 'Pt@Inf {}'.format(self.name)

    def __eq__(self, point_at_infinity):
        assert isinstance(point_at_infinity, PointAtInfinity)

        return self.direction.is_scalar_multiple(point_at_infinity.direction)


# alias
PtAtInf = PointAtInfinity
