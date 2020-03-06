from __future__ import annotations


__all__ = \
    'PointInR2', 'PointR2', 'Point', 'Pt', \
    'PointAtInfinityInR2', 'PointAtInfinityR2', 'PointAtInfinity', 'PointAtInf', 'PtAtInf'


from sympy.geometry.point import Point2D

from ....geom.var import Variable, OptionalVariableOrNumericType, VARIABLE_AND_NUMERIC_TYPES
from ...._util._compat import cached_property
from ...._util._tmp import TMP_NAME_FACTORY
from ...._util._type import NUMERIC_TYPES, OptionalStrOrCallableReturningStrType, print_obj_and_type
from .._abc._point import _EuclideanPointABC, _EuclideanConcretePointABC, _EuclideanPointAtInfinityABC
from ._abc._entity import _EuclideanGeometryEntityInR2ABC


class _PointInR2ABC(_EuclideanGeometryEntityInR2ABC, _EuclideanPointABC):
    pass


@_PointInR2ABC.assign_name_and_dependencies
class PointInR2(_PointInR2ABC, _EuclideanConcretePointABC, Point2D):
    def __new__(
            cls,
            x: OptionalVariableOrNumericType = None, y: OptionalVariableOrNumericType = None,
            *, name: OptionalStrOrCallableReturningStrType = TMP_NAME_FACTORY) \
            -> Point2D:
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

        point = super().__new__(
                    cls,
                    x, y,   # *coords
                    evaluate=False   # if True (default), all floats are turn into exact types
                )

        setattr(point, cls._NAME_ATTR_KEY, name)
        setattr(point, cls._DEPENDENCIES_ATTR_KEY, dependencies)

        return point

    @property
    def free(self) -> bool:
        return ((not isinstance(self.x, Variable)) or self.x.free) \
           and ((not isinstance(self.y, Variable)) or self.y.free)

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

    @name.deleter
    def name(self):
        self.name = TMP_NAME_FACTORY()

    def same(self) -> PointInR2:
        return PointInR2(self.x, self.y)

    @classmethod
    def _from_sympy_point_2d(cls, sympy_point_2d: Point2D, /) -> PointInR2:
        return cls(Variable(sympy_point_2d.x), Variable(sympy_point_2d.y))

    def __neg__(self) -> PointInR2:
        return self._from_sympy_point_2d(super().__neg__())

    def __add__(self, point: Point2D, /) -> PointInR2:
        return self._from_sympy_point_2d(super().__add__(point))

    def __sub__(self, point: Point2D, /) -> PointInR2:
        return self._from_sympy_point_2d(super().__sub__(point))

    def __mul__(self, n: Variable, /) -> PointInR2:
        return self._from_sympy_point_2d(super().__mul__(n))

    def __truediv__(self, n: Variable, /) -> PointInR2:
        return self._from_sympy_point_2d(super().__div__(n))

    def euclidean_distance(self, other_point_in_r2: PointInR2, /) -> Variable:
        return Variable((self.x - other_point_in_r2.x) ** 2 + (self.y - other_point_in_r2.y) ** 2)

    @cached_property
    def euclidean_distance_from_origin(self) -> Variable:
        return Variable(self.x ** 2 + self.y ** 2)


# aliases
Pt = Point = PointR2 = PointInR2


@_PointInR2ABC.assign_name_and_dependencies
class PointAtInfinityInR2(_PointInR2ABC, _EuclideanPointAtInfinityABC):
    def __init__(self, direction: PointInR2, /) -> None:
        assert isinstance(direction, PointInR2), \
            TypeError(f'*** DIRECTION {direction} NOT OF TYPE {PointInR2.__name__} ***')

        self.direction = direction


# aliases
PtAtInf = PointAtInf = PointAtInfinity = PointAtInfinityR2 = PointAtInfinityInR2
