"""Coordinate System classes."""


from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import ACoordSys
from .euclid import EuclidCoordSys, EUCLID_COORD_SYS

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('ACoordSys',
                                    'EuclidCoordSys', 'EUCLID_COORD_SYS')
