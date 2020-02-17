from __future__ import annotations


__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.geometry.point import Point3D

from ....geom.var import Variable, OptionalVariableType, VARIABLE_AND_NUMERIC_TYPES
from ....util.compat import cached_property
from ....util.tmp import TMP_NAME_FACTORY
from ....util.types import NUMERIC_TYPES, OptionalStrType, print_obj_and_type
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
            name = TMP_NAME_FACTORY()

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


class PointAtInfinityInR3(_PointInR3ABC, _EuclidPointAtInfinityABC):
    @_PointInR3ABC._with_dependency_tracking
    @_PointInR3ABC._with_name_assignment(tmp_if_empty=True)
    def __init__(self, direction: PointInR3, /) -> None:
        assert isinstance(direction, PointInR3), \
            TypeError(f'*** DIRECTION {direction} NOT {PointInR3.__name__} ***')

        self.direction = direction


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3
