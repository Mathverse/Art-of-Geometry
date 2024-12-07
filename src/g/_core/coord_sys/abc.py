"""Abstract Coordinate System."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import LiteralString

from ..variable import RealVarOrNum

from ..point.abc import APoint
from ..space.abc import _SpaceABC


__all__: Sequence[LiteralString] = ('ACoordSys',)


class ACoordSys:
    """Abstract Coordinate System."""

    @abstractmethod
    def __call__(self, point: APoint, space: _SpaceABC) -> tuple[RealVarOrNum]:
        """Return Point's coordinate in Space."""
        raise NotImplementedError
