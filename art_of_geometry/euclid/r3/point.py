__all__ = \
    'Point', 'Pt', \
    'PointAtInfinity', 'PtAtInf'


from sympy.core.symbol import Symbol
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.point import Point3D
from uuid import uuid4

from ... import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    pass


class Point(Point3D, _PointABC):
    def __new__(cls, x: Symbol = None, y: Symbol = None, z: Symbol = None, name: str = None):
        if not name:
            name = str(uuid4())

        if x is None:
            x = Symbol(name='{}.x'.format(name), real=True)

        if y is None:
            y = Symbol(name='{}.y'.format(name), real=True)
            
        if z is None:
            z = Symbol(name='{}.z'.format(name), real=True)

        point = super().__new__(
                    cls,
                    x, y, z,   # *coords
                    evaluate=False   # if True (default), all floats are turn into exact types
                )

        point._name = name

        return point

    def __repr__(self):
        return 'Pt {}'.format(self.name)

    @classmethod
    def _from_sympy_point_3d(cls, sympy_point_3d: Point3D, name: str = None):
        return cls(
                x=sympy_point_3d.x,
                y=sympy_point_3d.y,
                z=sympy_point_3d.z,
                name=name)


# alias
Pt = Point


class PointAtInfinity(_PointABC):
    def __init__(self, direction: Point, name: str = None):
        assert isinstance(direction, Point), \
            GeometryError(
                '*** DIRECTION {} NOT {} ***'
                .format(direction, Point.__name__))

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
