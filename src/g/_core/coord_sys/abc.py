"""Abstract Coordinate System."""


from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self

    from ..point import APoint
    from ..variable import NumOrVar


__all__: Sequence[LiteralString] = ('ACoordSys',)


class ACoordSys:
    """Abstract Coordinate System."""

    name: str

    @abstractmethod
    def __call__(self: Self, *coords: NumOrVar) -> APoint:
        """Return Point from coordinates."""
        raise NotImplementedError

    @abstractmethod
    def locate(self: Self, point: APoint) -> tuple[NumOrVar]:
        """Return Point's coordinates."""
        raise NotImplementedError
