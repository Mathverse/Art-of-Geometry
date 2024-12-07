"""Abstract Euclidean Geometry Entity."""


from __future__ import annotations

from typing import TYPE_CHECKING

from g._core import AGeomEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('AnEuclidGeomEntity',)


class AnEuclidGeomEntity(AGeomEntity):
    """Abstract Euclidean Geometry Entity."""
