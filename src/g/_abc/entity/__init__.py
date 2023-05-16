"""Entity."""


from collections.abc import Sequence
from typing import LiteralString

from .abstract import _EntityABC
from .decor import assign_entity_name_and_dependencies
from .geometry import _GeometryEntityABC


__all__: Sequence[LiteralString] = ('_EntityABC',
                                    'assign_entity_name_and_dependencies',
                                    '_GeometryEntityABC')
