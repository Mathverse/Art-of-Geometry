"""Abstract Point base classes."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import LiteralString

from .entity import _GeomEntityABC
from .vector import _VectorABC


__all__: Sequence[LiteralString] = ('_PointABC',
                                    '_ConcretePointABC',
                                    '_PointAtInfinityABC')


class _PointABC(_GeomEntityABC):
    """Abstract Point."""

    _NAME_NULLABLE: bool = False

    @abstractmethod
    def __eq__(self, other_point: _PointABC, /) -> bool:
        """Check equality."""
        raise NotImplementedError

    def __ne__(self, other_point: _PointABC, /) -> bool:
        """Check inequality."""
        return not self == other_point

    def __add__(self, vector: _VectorABC, /) -> _PointABC:
        """Add vector."""
        raise NotImplementedError

    def __radd__(self, vector: _VectorABC, /) -> _PointABC:
        """Add vector."""
        return self + vector


class _ConcretePointABC(_PointABC):
    """Abstract Concrete Point."""

    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @property
    @abstractmethod
    def free(self) -> bool:
        """Check freeness."""
        raise NotImplementedError


class _PointAtInfinityABC(_PointABC):
    """Abstract Point at Infinity."""

    @property
    def _short_repr(self) -> str:
        return f'Pt@Inf {self.name}'
