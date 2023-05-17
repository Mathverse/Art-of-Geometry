"""Entity."""


from collections.abc import Sequence
from typing import LiteralString

from .decor import assign_entity_dependencies_and_name
from .geom import _GeometryEntityABC


__all__: Sequence[LiteralString] = ('assign_entity_dependencies_and_name',
                                    '_GeometryEntityABC')
