from __future__ import annotations


__all__ = \
    'PointInR1', 'PointR1', 'Point', 'Pt', \
    'PointAtInfinityInR1', 'PointAtInfinityR1', 'PointAtInfinity', 'PtAtInf'


from sympy.core.singleton import S

from ...._util._tmp import TMP_NAME_FACTORY
from ...._util._type import NUMERIC_TYPES, OptionalStrOrCallableReturningStrType, print_obj_and_type
from ...var import Variable, OptionalVariableOrNumericType, VARIABLE_AND_NUMERIC_TYPES
from .._abc._point import _EuclideanConcretePointABC, _EuclideanPointAtInfinityABC


@_EuclideanConcretePointABC.assign_name_and_dependencies
class PointInR1(_EuclideanConcretePointABC):
    def __init__(
            self, x: OptionalVariableOrNumericType = None, /,
            *, name: OptionalStrOrCallableReturningStrType = TMP_NAME_FACTORY) \
            -> None:
        if callable(name):
            name = name()
        elif not name:
            name = TMP_NAME_FACTORY()
        self._validate_name(name)

        if x is None:
            x = Variable(f'[{name}.x]', real=True)
            dependencies = x,

        elif isinstance(x, Variable):
            dependencies = x,

        else:
            assert isinstance(x, NUMERIC_TYPES), \
                TypeError(f'*** X COORDINATE {print_obj_and_type(x)} '
                          f'NOT OF ONE OF TYPES {VARIABLE_AND_NUMERIC_TYPES} ***')

            dependencies = ()

        self.x = x

        setattr(self, self._NAME_ATTR_KEY, name)
        setattr(self, self._DEPENDENCIES_ATTR_KEY, dependencies)

    @property
    def free(self) -> bool:
        return (not isinstance(self.x, Variable)) or self.x.free

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

    @name.deleter
    def name(self):
        self.name = TMP_NAME_FACTORY()

    def euclidean_distance(self, other_euclidean_point: PointInR1, /) -> Variable:
        return Variable(abs(self.x - other_euclidean_point.x))

    def euclidean_distance_from_origin(self) -> Variable:
        return Variable(abs(self.x))


# aliases
Pt = Point = PointR1 = PointInR1


@_EuclideanConcretePointABC.assign_name_and_dependencies
class _PointAtInfinityInR1(_EuclideanPointAtInfinityABC):
    def __init__(self):
        self.direction = PointInR1(S.One)


# singleton aliases
PtAtInf = PointAtInfinity = PointAtInfinityR1 = PointAtInfinityInR1 = _PointAtInfinityInR1(name='∞')
