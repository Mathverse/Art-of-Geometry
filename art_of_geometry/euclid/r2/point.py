__all__ = \
    'PointInR2', 'PointR2', 'Point', 'Pt', \
    'PointAtInfinityInR2', 'PointAtInfinityR2', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.core.symbol import Symbol
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.point import Point2D
from uuid import uuid4

from . import _EuclidR2GeometryEntityABC


class _PointInR2ABC(_EuclidR2GeometryEntityABC):
    pass


class PointInR2(_PointInR2ABC, Point2D):
    def __new__(cls, x: Symbol = None, y: Symbol = None, name: str = None) -> Point2D:
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

        point = super().__new__(
                    cls,
                    x, y,   # *coords
                    evaluate=False   # if True (default), all floats are turn into exact types
                )

        point._name = name

        return point

    def __repr__(self) -> str:
        return 'Pt {}'.format(self.name)


# aliases
Pt = Point = PointR2 = PointInR2


class PointAtInfinityInR2(_PointInR2ABC):
    def __init__(self, direction: Point2D, name: str = None) -> None:
        assert isinstance(direction, Point2D), \
            GeometryError(
                '*** DIRECTION {} NOT OF TYPE {} ***'
                .format(direction, Point2D.__name__))

        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())

    def __repr__(self) -> str:
        return 'Pt@Inf {}'.format(self.name)

    def __eq__(self, point_at_infinity) -> bool:
        assert isinstance(point_at_infinity, PointAtInfinityInR2)

        return self.direction.is_scalar_multiple(point_at_infinity.direction)


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR2 = PointAtInfinityInR2
