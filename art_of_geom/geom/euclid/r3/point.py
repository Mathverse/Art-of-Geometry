__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.point import Point3D
from typing import Optional
from uuid import uuid4

from ....util.compat import cached_property
from ..point import _EuclidPointABC, _EuclidConcretePointABC, _EuclidPointAtInfinityABC
from .abc import _EuclidGeometryEntityInR3ABC


class _PointInR3ABC(_EuclidGeometryEntityInR3ABC, _EuclidPointABC):
    pass


class PointInR3(_PointInR3ABC, _EuclidConcretePointABC, Point3D):
    def __new__(
            cls,
            /, x: Optional[Expr] = None, y: Optional[Expr] = None, z: Optional[Expr] = None,
            *, name: Optional[str] = None) \
            -> Point3D:
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
            
        if z is None:
            z = Symbol(
                    name=f'[{name}.z]',
                    real=True)
        else:
            assert isinstance(z, (Expr, float, int)), \
                TypeError(f'*** Z COORDINATE {z} NEITHER SymPy Expr NOR float NOR int ***')

        point = super().__new__(
                    cls,
                    x, y, z,   # *coords
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

            if isinstance(self.z, Symbol):
                self.z.name = f'[{name}.z]'

    @_PointInR3ABC._with_name_assignment
    def same(self) -> 'PointInR3':
        return PointInR3(self.x, self.y, self.z)

    @classmethod
    @_PointInR3ABC._with_name_assignment
    def _from_sympy_point_3d(cls, sympy_point_3d: Point3D, /) -> 'PointInR3':
        return PointInR3(sympy_point_3d.x, sympy_point_3d.y, sympy_point_3d.z)

    def __neg__(self) -> 'PointInR3':
        return self._from_sympy_point_3d(super().__neg__())

    def __add__(self, point: Point3D, /) -> 'PointInR3':
        return self._from_sympy_point_3d(super().__add__(point))

    def __sub__(self, point: Point3D, /) -> 'PointInR3':
        return self._from_sympy_point_3d(super().__sub__(point))

    def __mul__(self, n: Expr, /) -> 'PointInR3':
        return self._from_sympy_point_3d(super().__mul__(n))

    def __div__(self, n: Expr, /) -> 'PointInR3':
        return self._from_sympy_point_3d(super().__div__(n))

    @cached_property
    def distance_from_origin(self) -> Expr:
        return self.x ** 2 + self.y ** 2 + self.z ** 2


# aliases
Pt = Point = PointR3 = PointInR3


class PointAtInfinityInR3(_PointInR3ABC, _EuclidPointAtInfinityABC):
    def __init__(
            self,
            direction: Point3D, /,
            *, name: Optional[str] = None) \
            -> None:
        assert isinstance(direction, Point3D), \
            TypeError(f'*** DIRECTION {direction} NOT {Point3D.__name__} ***')

        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3
