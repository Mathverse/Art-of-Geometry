"""Abstract Point base classes.

Points are fundamental geometric entities.
"""


from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from .._entity import AGeomEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self

    from ..vector import Vector


__all__: Sequence[LiteralString] = 'APoint', 'AConcretePoint', 'APointAtInf'


class APoint(AGeomEntity):
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
