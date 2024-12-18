"""Entity classes & decorators."""


from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import AnEntity
from .decor import assign_entity_dependencies_and_name
from .geom import AGeomEntity
from .non_geom import ANonGeomEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('AnEntity', 'AGeomEntity', 'ANonGeomEntity',  # noqa: E501
                                    'assign_entity_dependencies_and_name')
