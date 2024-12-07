"""Abstract base classes & fundamental concepts."""


from typing import TYPE_CHECKING

from ._entity import AGeomEntity, ANonGeomEntity, assign_entity_dependencies_and_name  # noqa: E501

from .coord_sys import ACoordSys

from .point import APoint, AConcretePoint, APointAtInf

from .space import (ASpace,
                    ASubSpace, AHalfSpace, AClosedSubSpace,

                    ALinearEntity,
                    AConcreteLinearEntity,
                    ALinearEntityAtInf,

                    ALine,

                    AConcreteLine,
                    AConcreteDirectedLine,

                    ALineAtInf,
                    ADirectedLineAtInf)

from .variable import (Variable, Var,
                       RealVariable, RealVar,
                       NumOrVar, OptionalNumOrVar,
                       RealNumOrVar, OptionalRealNumOrVar)

from .vector import (Vector, Vec, V,
                     Ux, Uy, Uz, V0)


if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = (
    'AGeomEntity', 'ANonGeomEntity', 'assign_entity_dependencies_and_name',

    'ACoordSys',

    'APoint', 'AConcretePoint', 'APointAtInf',

    'ASpace',
    'ASubSpace', 'AHalfSpace', 'AClosedSubSpace',

    'ALinearEntity',
    'AConcreteLinearEntity',
    'ALinearEntityAtInf',

    'ALine',

    'AConcreteLine',
    'AConcreteDirectedLine',

    'ALineAtInf',
    'ADirectedLineAtInf',

    'Variable', 'Var',
    'RealVariable', 'RealVar',
    'NumOrVar', 'OptionalNumOrVar',
    'RealNumOrVar', 'OptionalRealNumOrVar',

    'Vector', 'Vec', 'V',
    'Ux', 'Uy', 'Uz', 'V0',
)
