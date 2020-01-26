__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from functools import cached_property
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.exceptions import GeometryError
from sympy.geometry.point import Point3D
from uuid import uuid4

from ..point import _EuclidPointABC, _EuclidConcretePointABC, _EuclidPointAtInfinityABC
from . import _EuclidGeometryEntityInR3ABC


class _PointInR3ABC(_EuclidGeometryEntityInR3ABC, _EuclidPointABC):
    pass


class PointInR3(_PointInR3ABC, _EuclidConcretePointABC, Point3D):
    def __new__(cls, /, x: Expr = None, y: Expr = None, z: Expr = None, *, name: str = None) -> Point3D:
        if not name:
            name = str(uuid4())

        if x is None:
            x = Symbol(
                    name='[{}.x]'.format(name),
                    real=True)
        else:
            assert isinstance(x, (Expr, float, int)), \
                TypeError(
                    '*** X COORDINATE {} NEITHER SymPy Expr NOR int NOR float ***'
                    .format(x))

        if y is None:
            y = Symbol(
                    name='[{}.y]'.format(name),
                    real=True)
        else:
            assert isinstance(y, (Expr, float, int)), \
                TypeError(
                    '*** Y COORDINATE {} NEITHER SymPy Expr NOR int NOR float ***'
                    .format(y))
            
        if z is None:
            z = Symbol(
                    name='[{}.z]'.format(name),
                    real=True)
        else:
            assert isinstance(z, (Expr, float, int)), \
                TypeError(
                    '*** Z COORDINATE {} NEITHER SymPy Expr NOR int NOR float ***'
                    .format(z))

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

            if isinstance(self.z, Symbol):
                self.z.name = '[{}.z]'.format(name)

    def same(self, *, name=None):
        return PointInR3(
                x=self.x,
                y=self.y,
                z=self.z,
                name=name)

    @classmethod
    def _from_sympy_point_3d(cls, sympy_point_3d: Point3D, /, *, name=None):
        return PointInR3(
                x=sympy_point_3d.x,
                y=sympy_point_3d.y,
                z=sympy_point_3d.z,
                name=name)

    def __neg__(self):
        return self._from_sympy_point_3d(
                super().__neg__())

    def __add__(self, point: Point3D, /):
        return self._from_sympy_point_3d(
                super().__add__(point))

    def __sub__(self, point: Point3D, /):
        return self._from_sympy_point_3d(
                super().__sub__(point))

    def __mul__(self, n: Expr, /):
        return self._from_sympy_point_3d(
                super().__mul__(n))

    def __div__(self, n: Expr, /):
        return self._from_sympy_point_3d(
                super().__div__(n))

    @cached_property
    def distance_from_origin(self) -> Expr:
        return self.x ** 2 + self.y ** 2 + self.z ** 2


# aliases
Pt = Point = PointR3 = PointInR3


class PointAtInfinityInR3(_PointInR3ABC, _EuclidPointAtInfinityABC):
    def __init__(self, direction: Point3D, /, *, name: str = None) -> None:
        assert isinstance(direction, Point3D), \
            TypeError(
                '*** DIRECTION {} NOT {} ***'
                .format(direction, Point3D.__name__))

        self.direction = direction

        self._name = \
            name \
            if name \
            else str(uuid4())


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3