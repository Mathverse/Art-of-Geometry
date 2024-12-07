"""Abstract Non-Geometric Entity.

Examples of non-geometric entities include numerical Variables, which represent
numbers, and Vectors, which represent directions and magnitudes/strengths but
are not tied to any location in space.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import AnEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('ANonGeomEntity',)


class ANonGeomEntity(AnEntity):
    """Abstract Non-Geometric Entity."""
