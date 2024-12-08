"""Abstract Coordinate System."""


from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self

    from ..point import APoint
    from ..variable import NumOrVar
    from .type import Coords


__all__: Sequence[LiteralString] = ('ACoordSys',)


class ACoordSys:
    """Abstract Coordinate System."""

    @abstractmethod
    def __call__(self: Self, *coords: NumOrVar, **kw_coords: NumOrVar) -> APoint:  # noqa: E501
        """Return Point from coordinates."""
        raise NotImplementedError

    @abstractmethod
    def locate(self: Self, point: APoint) -> Coords:
        """Return Point's coordinates."""
        raise NotImplementedError
