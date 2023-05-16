"""Entity."""


from collections.abc import Sequence
from typing import LiteralString

from .abc import _EntityABC
from .decor import assign_entity_name_and_dependencies
from .geom import _GeometryEntityABC


__all__: Sequence[LiteralString] = ('_EntityABC',
                                    'assign_entity_name_and_dependencies',
                                    '_GeometryEntityABC')
