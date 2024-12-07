"""Abstract Point base classes.

Points are fundamental geometric entities.

Each Point can belong to multiple Spaces, in each of which it can have a set of
locational coordinates.
"""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import LiteralString, Self

from .._entity.geom import _GeomEntityABC
from ..vector import Vector


__all__: Sequence[LiteralString] = 'APoint', 'AConcretePoint', 'APointAtInf'


class APoint(_GeomEntityABC):
    """Abstract Point."""

    _NAME_NULLABLE: bool = False

    @abstractmethod
    def __eq__(self, other_point: APoint, /) -> bool:
        """Check equality."""
        raise NotImplementedError

    def __ne__(self, other_point: APoint, /) -> bool:
        """Check inequality."""
        return not self == other_point

    def __add__(self, vector: Vector, /) -> Self:
        """Add vector."""
        raise NotImplementedError

    def __radd__(self, vector: Vector, /) -> Self:
        """Add vector."""
        return self + vector

    def point(self) -> Self:
        """Pick itself."""
        return self


class AConcretePoint(APoint):
    """Abstract Concrete Point."""

    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @property
    @abstractmethod
    def free(self) -> bool:
        """Check freeness."""
        raise NotImplementedError


class APointAtInf(APoint):
    """Abstract Point at Infinity."""

    @property
    def _short_repr(self) -> str:
        return f'Pt@Inf {self.name}'
