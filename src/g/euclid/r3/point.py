from __future__ import annotations


__all__ = \
    'PointInR3', 'PointR3', 'Point', 'Pt', \
    'PointAtInfinityInR3', 'PointAtInfinityR3', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.geometry.point import Point3D

from ....geom.var import Variable, OptionalVariableOrNumericType, VARIABLE_AND_NUMERIC_TYPES
from ...._util._compat import cached_property
from ...._util._tmp import TMP_NAME_FACTORY
from ...._util._type import NUMERIC_TYPES, OptionalStrOrCallableReturningStrType, print_obj_and_type
from .._abc._point import _EuclideanPointABC, _EuclideanConcretePointABC, _EuclideanPointAtInfinityABC
from ._abc._entity import _EuclideanGeometryEntityInR3ABC


class _PointInR3ABC(_EuclideanGeometryEntityInR3ABC, _EuclideanPointABC):
    pass


@_PointInR3ABC.assign_name_and_dependencies
class PointInR3(_PointInR3ABC, _EuclideanConcretePointABC, Point3D):
    def __new__(
            cls,
            /, x: OptionalVariableOrNumericType = None,
               y: OptionalVariableOrNumericType = None,
               z: OptionalVariableOrNumericType = None,
            *, name: OptionalStrOrCallableReturningStrType = TMP_NAME_FACTORY) \
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

        setattr(point, cls._NAME_ATTR_KEY, name)
        setattr(point, cls._DEPENDENCIES_ATTR_KEY, dependencies)

        return point

    @property
    def free(self) -> bool:
        return ((not isinstance(self.x, Variable)) or self.x.free) \
           and ((not isinstance(self.y, Variable)) or self.y.free) \
           and ((not isinstance(self.z, Variable)) or self.z.free)

    @property
    def name(self) -> str:
        return getattr(self, self._NAME_ATTR_KEY)

    @name.setter
    def name(self, name: str, /) -> None:
        self._validate_name(name)

        if name != getattr(self, self._NAME_ATTR_KEY):
            setattr(self, self._NAME_ATTR_KEY, name)

            if isinstance(self.x, Variable):
                self.x.name = f'[{name}.x]'

            if isinstance(self.y, Variable):
                self.y.name = f'[{name}.y]'

            if isinstance(self.z, Variable):
                self.z.name = f'[{name}.z]'

    @name.deleter
    def name(self):
        self.name = TMP_NAME_FACTORY()

    def same(self) -> PointInR3:
        return PointInR3(self.x, self.y, self.z)

    @classmethod
    def _from_sympy_point_3d(cls, sympy_point_3d: Point3D, /) -> PointInR3:
        return cls(Variable(sympy_point_3d.x), Variable(sympy_point_3d.y), Variable(sympy_point_3d.z))

    def __neg__(self) -> PointInR3:
        return self._from_sympy_point_3d(super().__neg__())

    def __add__(self, point: Point3D, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__add__(point))

    def __sub__(self, point: Point3D, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__sub__(point))

    def __mul__(self, n: Variable, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__mul__(n))

    def __truediv__(self, n: Variable, /) -> PointInR3:
        return self._from_sympy_point_3d(super().__div__(n))

    def euclidean_distance(self, other_point_in_r3: _EuclideanPointABC, /) -> Variable:
        return Variable((self.x - other_point_in_r3.x) ** 2 +
                        (self.y - other_point_in_r3.y) ** 2 +
                        (self.z - other_point_in_r3.z) ** 2)

    @cached_property
    def euclidean_distance_from_origin(self) -> Variable:
        return Variable(self.x ** 2 + self.y ** 2 + self.z ** 2)


# aliases
Pt = Point = PointR3 = PointInR3


@_PointInR3ABC.assign_name_and_dependencies
class PointAtInfinityInR3(_PointInR3ABC, _EuclideanPointAtInfinityABC):
    def __init__(self, direction: PointInR3, /) -> None:
        assert isinstance(direction, PointInR3), \
            TypeError(f'*** DIRECTION {direction} NOT {PointInR3.__name__} ***')

        self.direction = direction


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR3 = PointAtInfinityInR3
