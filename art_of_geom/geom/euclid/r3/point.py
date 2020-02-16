from __future__ import annotations


__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.geometry.point import Point3D
from typing import Optional
from uuid import uuid4

from ....geom.var import Variable, OptionalVariableType, VariableOrNumericType
from ....util.compat import cached_property
from ....util.types import OptionalStrType, print_obj_and_type
from ..point import _EuclidPointABC, _EuclidConcretePointABC, _EuclidPointAtInfinityABC
from .abc import _EuclidGeometryEntityInR3ABC


class _PointInR3ABC(_EuclidGeometryEntityInR3ABC, _EuclidPointABC):
    pass


class PointInR3(_PointInR3ABC, _EuclidConcretePointABC, Point3D):
    def __new__(
            cls,
            /, x: OptionalVariableType = None, y: OptionalVariableType = None, z: OptionalVariableType = None,
            *, name: OptionalStrType = None) \
            -> Point3D:
        if not name:
            name = str(uuid4())

        if x is None:
            x = Variable(f'[{name}.x]', real=True)
        else:
            assert isinstance(x, VariableOrNumericType), \
                TypeError(f'*** X COORDINATE {print_obj_and_type(x)} NOT OF TYPE {VariableOrNumericType} ***')

        if y is None:
            y = Variable(f'[{name}.y]', real=True)
        else:
            assert isinstance(y, VariableOrNumericType), \
                TypeError(f'*** Y COORDINATE {print_obj_and_type(y)} NOT OF TYPE {VariableOrNumericType} ***')
            
        if z is None:
            z = Variable(f'[{name}.z]', real=True)
        else:
            assert isinstance(z, VariableOrNumericType), \
                TypeError(f'*** Z COORDINATE {print_obj_and_type(z)} NOT OF TYPE {VariableOrNumericType} ***')

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

            if isinstance(self.x, Variable):
                self.x.name = f'[{name}.x]'

            if isinstance(self.y, Variable):
                self.y.name = f'[{name}.y]'

            if isinstance(self.z, Variable):
                self.z.name = f'[{name}.z]'

    @_PointInR3ABC._with_name_assignment
    def same(self) -> PointInR3:
        return PointInR3(self.x, self.y, self.z)

    @classmethod
    @_PointInR3ABC._with_name_assignment
    def _from_sympy_point_3d(cls, sympy_point_3d: Point3D, /) -> PointInR3:
        return PointInR3(sympy_point_3d.x, sympy_point_3d.y, sympy_point_3d.z)

    def __neg__(self) -> PointInR3:
        return self._from_sympy_point_3d(super().__neg__())

    def __add__(self, point: Point3D, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__add__(point))

    def __sub__(self, point: Point3D, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__sub__(point))

    def __mul__(self, n: Variable, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__mul__(n))

    def __div__(self, n: Variable, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__div__(n))

    @cached_property
    def distance_from_origin(self) -> Variable:
        return Variable(self.x ** 2 + self.y ** 2 + self.z ** 2)


# aliases
Pt = Point = PointR3 = PointInR3


class PointAtInfinityInR3(_PointInR3ABC, _EuclidPointAtInfinityABC):
    @_PointInR3ABC._with_name_assignment(uuid_if_empty=True)
    def __init__(self, direction: Point3D, /) -> None:
        assert isinstance(direction, Point3D), \
            TypeError(f'*** DIRECTION {direction} NOT {Point3D.__name__} ***')

        self.direction = direction


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3
