"""Abstract Vector."""


from collections.abc import Sequence
from dataclasses import dataclass
from typing import LiteralString

from .._util.type import Num
from .entity import _GeomEntityABC


__all__: Sequence[LiteralString] = ('_VectorABC',)


@dataclass
class _VectorABC(_GeomEntityABC):
    """Abstract Vector."""

    coordinates: tuple[Num]
