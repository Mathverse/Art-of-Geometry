from __future__ import annotations


__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.geometry.point import Point3D

from ....geom.var import Variable, OptionalVariableOrNumericType, VARIABLE_AND_NUMERIC_TYPES
from ...._util._compat import cached_property
from ...._util._tmp import TMP_NAME_FACTORY
from ...._util._type import NUMERIC_TYPES, OptionalStrOrCallableReturningStrType, print_obj_and_type
from art_of_geom.geom.euclid._abc._point import _EuclidPointABC, _EuclidConcretePointABC, _EuclidPointAtInfinityABC
from .abc import _EuclidGeometryEntityInR3ABC


class _PointInR3ABC(_EuclidGeometryEntityInR3ABC, _EuclidPointABC):
    pass


@_PointInR3ABC.assign_name_and_dependencies
class PointInR3(_PointInR3ABC, _EuclidConcretePointABC, Point3D):
    def __new__(
            cls,
            /, x: OptionalVariableOrNumericType = None, y: OptionalVariableOrNumericType = None, z: OptionalVariableOrNumericType = None,
            *, name: OptionalStrOrCallableReturningStrType = None) \
            -> Point3D:
        if callable(name):
            name = name()
        elif not name:
            name = TMP_NAME_FACTORY()
        cls._validate_name(name)

        dependencies = []

        if x is None:
            x = Variable(f'[{name}.x]', real=True)
            dependencies.append(x)

        elif isinstance(x, Variable):
            dependencies.append(x)

        else:
            assert isinstance(x, NUMERIC_TYPES), \
                TypeError(f'*** X COORDINATE {print_obj_and_type(x)} '
                          f'NOT OF ONE OF TYPES {VARIABLE_AND_NUMERIC_TYPES} ***')

        if y is None:
            y = Variable(f'[{name}.y]', real=True)
            dependencies.append(y)

        elif isinstance(y, Variable):
            dependencies.append(y)

        else:
            assert isinstance(y, NUMERIC_TYPES), \
                TypeError(f'*** Y COORDINATE {print_obj_and_type(y)} '
                          f'NOT OF ONE OF TYPES {VARIABLE_AND_NUMERIC_TYPES} ***')
            
        if z is None:
            z = Variable(f'[{name}.z]', real=True)
            dependencies.append(z)

        elif isinstance(z, Variable):
            dependencies.append(z)

        else:
            assert isinstance(z, NUMERIC_TYPES), \
                TypeError(f'*** Z COORDINATE {print_obj_and_type(z)} '
                          f'NOT OF ONE OF TYPES {VARIABLE_AND_NUMERIC_TYPES} ***')

        point = super().__new__(
                    cls,
                    x, y, z,   # *coords
                    evaluate=False   # if True (default), all floats are turn into exact types
                )

        point._name = name

        point._dependencies = dependencies

        return point

    @property
    def free(self) -> bool:
        return ((not isinstance(self.x, Variable)) or self.x.free) \
           and ((not isinstance(self.y, Variable)) or self.y.free) \
           and ((not isinstance(self.z, Variable)) or self.z.free)

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

    def same(self) -> PointInR3:
        return PointInR3(self.x, self.y, self.z)

    @staticmethod
    def _from_sympy_point_3d(sympy_point_3d: Point3D, /) -> PointInR3:
        return PointInR3(Variable(sympy_point_3d.x), Variable(sympy_point_3d.y), Variable(sympy_point_3d.z))

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


@_PointInR3ABC.assign_name_and_dependencies
class PointAtInfinityInR3(_PointInR3ABC, _EuclidPointAtInfinityABC):
    def __init__(self, direction: PointInR3, /) -> None:
        assert isinstance(direction, PointInR3), \
            TypeError(f'*** DIRECTION {direction} NOT {PointInR3.__name__} ***')

        self.direction = direction


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3
