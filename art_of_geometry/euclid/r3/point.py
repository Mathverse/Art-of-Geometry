__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.core.symbol import Symbol
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.point import Point3D
from uuid import uuid4

from . import _EuclidR3GeometryEntityABC


class _PointInR3ABC(_EuclidR3GeometryEntityABC):
    pass


class PointInR3(_PointInR3ABC, Point3D):
    def __new__(cls, x: Symbol = None, y: Symbol = None, z: Symbol = None, name: str = None) -> Point3D:
        if not name:
            name = str(uuid4())

        if x is None:
            x = Symbol(
                    name='[{}.x]'.format(name),
                    real=True)

        if y is None:
            y = Symbol(
                    name='[{}.y]'.format(name),
                    real=True)
            
        if z is None:
            z = Symbol(
                    name='[{}.z]'.format(name),
                    real=True)

        point = super().__new__(
                    cls,
                    x, y, z,   # *coords
                    evaluate=False   # if True (default), all floats are turn into exact types
                )

        point._name = name

        return point

    def __repr__(self) -> str:
        return 'Pt {}'.format(self.name)


# aliases
Pt = Point = PointR3 = PointInR3


class PointAtInfinityInR3(_PointInR3ABC):
    def __init__(self, direction: Point3D, name: str = None) -> None:
        assert isinstance(direction, Point3D), \
            GeometryError(
                '*** DIRECTION {} NOT {} ***'
                .format(direction, Point3D.__name__))

        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self) -> str:
        return 'Pt@Inf {}'.format(self.name)

    def __eq__(self, point_at_infinity) -> bool:
        assert isinstance(point_at_infinity, PointAtInfinityInR3)

        return self.direction.is_scalar_multiple(point_at_infinity.direction)


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3
