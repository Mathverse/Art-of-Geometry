"""Abstract Coordinate System."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self

    from ..point import APoint
    from ..variable import NumOrVar
    from .type import Coords


__all__: Sequence[LiteralString] = ('ACoordSys',)


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=True,  # force hashing using unique name
           frozen=True,  # TODO: decide whether immutability is necessary
           match_args=True,
           kw_only=False,
           slots=False,
           weakref_slot=False)
class ACoordSys(ABC):
    """Abstract Coordinate System."""

    name: str

    @abstractmethod
    def __call__(self: Self, *coords: NumOrVar, **kw_coords: NumOrVar) -> APoint:  # noqa: E501
        """Return Point from coordinates."""
        raise NotImplementedError

    @abstractmethod
    def locate(self: Self, point: APoint) -> Coords:
        """Return Point's coordinates."""
        raise NotImplementedError
