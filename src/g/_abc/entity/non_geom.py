"""Abstract Non-Geometric Entity.

Examples of non-geometric entities include numerical Variables, which represent
numbers, and Vectors, which represent directions and magnitudes/strengths but
are not tied to any location in space.
"""


from collections.abc import Sequence
from typing import LiteralString

from .abc import _EntityABC


__all__: Sequence[LiteralString] = ('_NonGeomEntityABC',)


class _NonGeomEntityABC(_EntityABC):
    """Abstract Non-Geometric Entity."""
