__all__ = \
    'Point', 'Pt', \
    'PointAtUndirectedInfinity', 'PtAtUndirInf', \
    'PointAtDirectedInfinity', 'PtAtDirInf'


from sympy.core.singleton import S
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


class PointAtUndirectedInfinity(_PointABC):
    def __init__(self, direction, name=None):
        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self):
        return 'Pt@UndirInf {}'.format(self.name)

    def __eq__(self, point_at_undirected_infinity):
        assert isinstance(point_at_undirected_infinity, PointAtUndirectedInfinity)

        return self.direction.is_scalar_multiple(point_at_undirected_infinity.direction)


# alias
PtAtUndirInf = PointAtUndirectedInfinity


class PointAtDirectedInfinity(_PointABC):
    def __init__(self, direction, name=None):
        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self):
        return 'Pt@DirInf {}'.format(self.name)


# alias
PtAtDirInf = PointAtDirectedInfinity
