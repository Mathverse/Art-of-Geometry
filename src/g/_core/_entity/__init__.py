"""Entity classes & decorators."""


from typing import TYPE_CHECKING

from .decor import assign_entity_dependencies_and_name
from .geom import AGeomEntity
from .non_geom import ANonGeomEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('AGeomEntity', 'ANonGeomEntity',
                                    'assign_entity_dependencies_and_name')
