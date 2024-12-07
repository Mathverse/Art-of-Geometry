"""Abstract Coordinate System."""


from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString

    from ..point import APoint
    from ..variable import RealVarOrNum


__all__: Sequence[LiteralString] = ('ACoordSys',)


class ACoordSys:
    """Abstract Coordinate System."""

    @abstractmethod
    def __call__(self, point: APoint) -> tuple[RealVarOrNum]:
        """Return Point's coordinates."""
        raise NotImplementedError
