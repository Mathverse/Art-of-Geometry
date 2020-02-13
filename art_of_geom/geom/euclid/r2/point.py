__all__ = \
    'PointInR2', 'PointR2', 'Point', 'Pt', \
    'PointAtInfinityInR2', 'PointAtInfinityR2', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.point import Point2D
from typing import Optional
from uuid import uuid4

from ....util.compat import cached_property
from ..point import _EuclidPointABC, _EuclidConcretePointABC, _EuclidPointAtInfinityABC
from .abc import _EuclidGeometryEntityInR2ABC


class _PointInR2ABC(_EuclidGeometryEntityInR2ABC, _EuclidPointABC):
    pass


class PointInR2(_PointInR2ABC, _EuclidConcretePointABC, Point2D):
    def __new__(
            cls,
            x: Optional[Expr] = None, y: Optional[Expr] = None,
            *, name: Optional[str] = None) \
            -> Point2D:
        if not name:
            name = str(uuid4())

        if x is None:
            x = Symbol(
                    name=f'[{name}.x]',
                    real=True)
        else:
            assert isinstance(x, (Expr, float, int)), \
                TypeError(f'*** X COORDINATE {x} NEITHER SymPy Expr NOR float NOR int ***')

        if y is None:
            y = Symbol(
                    name=f'[{name}.y]',
                    real=True)
        else:
            assert isinstance(y, (Expr, float, int)), \
                TypeError(f'*** Y COORDINATE {y} NEITHER SymPy Expr NOR float NOR int ***')

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
        self._validate_name(name)

        if name != self.name:
            self._name = name

            if isinstance(self.x, Symbol):
                self.x.name = f'[{name}.x]'

            if isinstance(self.y, Symbol):
                self.y.name = f'[{name}.y]'

    @_PointInR2ABC._with_name_assignment
    def same(self) -> 'PointInR2':
        return PointInR2(self.x, self.y)

    @classmethod
    @_PointInR2ABC._with_name_assignment
    def _from_sympy_point_2d(cls, sympy_point_2d: Point2D, /):
        return PointInR2(sympy_point_2d.x, sympy_point_2d.y)

    def __neg__(self) -> 'PointInR2':
        return self._from_sympy_point_2d(super().__neg__())

    def __add__(self, point: Point2D, /) -> 'PointInR2':
        return self._from_sympy_point_2d(super().__add__(point))

    def __sub__(self, point: Point2D, /) -> 'PointInR2':
        return self._from_sympy_point_2d(super().__sub__(point))

    def __mul__(self, n: Expr, /) -> 'PointInR2':
        return self._from_sympy_point_2d(super().__mul__(n))

    def __div__(self, n: Expr, /) -> 'PointInR2':
        return self._from_sympy_point_2d(super().__div__(n))

    @cached_property
    def distance_from_origin(self) -> Expr:
        return self.x ** 2 + self.y ** 2


# aliases
Pt = Point = PointR2 = PointInR2


class PointAtInfinityInR2(_PointInR2ABC, _EuclidPointAtInfinityABC):
    @_PointInR2ABC._with_name_assignment(uuid_if_empty=True)
    def __init__(self, direction: Point2D, /) -> None:
        assert isinstance(direction, Point2D), \
            TypeError(f'*** DIRECTION {direction} NOT OF TYPE {Point2D.__name__} ***')

        self.direction = direction


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR2 = PointAtInfinityInR2
