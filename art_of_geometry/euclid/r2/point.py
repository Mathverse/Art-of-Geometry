__all__ = \
    'PointInR2', 'PointR2', 'Point', 'Pt', \
    'PointAtInfinityInR2', 'PointAtInfinityR2', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from functools import cached_property
from sympy.core.expr import Expr
from sympy.core.numbers import oo
from sympy.core.symbol import Symbol
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.point import Point2D
from uuid import uuid4

from ...point import _PointABC
from . import _EuclidR2GeometryEntityABC


class _PointInR2ABC(_EuclidR2GeometryEntityABC, _PointABC):
    pass


class PointInR2(_PointInR2ABC, Point2D):
    def __new__(cls, /, x: Expr = None, y: Expr = None, *, name: str = None) -> Point2D:
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

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str, /) -> None:
        if name != self.name:
            assert isinstance(name, str) and name, \
                TypeError(
                    '*** {} NOT NON-EMPTY STRING ***'
                    .format(name))

            self._name = name

            if isinstance(self.x, Symbol):
                self.x.name = '[{}.x]'.format(name)

            if isinstance(self.y, Symbol):
                self.y.name = '[{}.y]'.format(name)

    def __repr__(self) -> str:
        return 'Pt {}'.format(self.name)

    def same(self, *, name=None):
        return PointInR2(
                x=self.x,
                y=self.y,
                name=name)

    @classmethod
    def _from_sympy_point_2d(cls, sympy_point_2d: Point2D, /, *, name=None):
        return PointInR2(
                x=sympy_point_2d.x,
                y=sympy_point_2d.y,
                name=name)

    def __neg__(self):
        return self._from_sympy_point_2d(
                super().__neg__())

    def __add__(self, point: Point2D, /):
        return self._from_sympy_point_2d(
                super().__add__(point))

    def __sub__(self, point: Point2D, /):
        return self._from_sympy_point_2d(
                super().__sub__(point))

    def __mul__(self, n: float, /):
        return self._from_sympy_point_2d(
                super().__mul__(n))

    def __div__(self, n: float, /):
        return self._from_sympy_point_2d(
                super().__div__(n))

    @cached_property
    def distance_from_origin(self) -> Expr:
        return self.x ** 2 + self.y ** 2


# aliases
Pt = Point = PointR2 = PointInR2


class PointAtInfinityInR2(_PointInR2ABC):
    def __init__(self, direction: Point2D, /, *, name: str = None) -> None:
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

    def __eq__(self, point_at_infinity, /) -> bool:
        assert isinstance(point_at_infinity, PointAtInfinityInR2), \
            GeometryError(
                '*** POINT_AT_INFINITY {} NOT OF TYPE {} ***'
                .format(point_at_infinity, PointAtInfinityInR2.__name__))

        return self.direction.is_scalar_multiple(point_at_infinity.direction)

    def same(self, *, name=None):
        return PointAtInfinityInR2(
                self.direction,
                name=name)

    @cached_property
    def distance_from_origin(self) -> Expr:
        return oo


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR2 = PointAtInfinityInR2
