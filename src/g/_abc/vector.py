"""Abstract Vector."""


from collections.abc import Sequence
from typing import LiteralString

from .entity import _GeomEntityABC


__all__: Sequence[LiteralString] = ('_VectorABC',)


class _VectorABC(_GeomEntityABC):
    """Abstract Vector."""
