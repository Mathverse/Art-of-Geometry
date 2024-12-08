"""Coordinates types."""


from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString

    from ..variable import NumOrVar
    from .euclid import EuclidCoords


__all__: Sequence[LiteralString] = ('Coords',)


Coords: type = tuple[NumOrVar] | dict[str, NumOrVar] | EuclidCoords
