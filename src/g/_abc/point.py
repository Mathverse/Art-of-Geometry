"""Point abtract base classes."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from typing import LiteralString

from ._entity import _GeomEntityABC


__all__: Sequence[LiteralString] = ('_PointABC',
                                    '_ConcretePointABC',
                                    '_PointAtInfinityABC')


class _PointABC(_GeomEntityABC):
    """Point abstract base class."""

    _NAME_NULLABLE = False

    @abstractmethod
    def __eq__(self, other_point: _PointABC, /) -> bool:
        """Check equality."""
        raise NotImplementedError

    def __ne__(self, other_point: _PointABC, /) -> bool:
        """Check inequality."""
        return not self == other_point


class _ConcretePointABC(_PointABC):
    """Concrete Point abstract base class."""

    @property
    def _short_repr(self) -> str:
        return f'Pt {self.name}'

    @property
    @abstractmethod
    def free(self) -> bool:
        """Check freeness."""
        raise NotImplementedError


class _PointAtInfinityABC(_PointABC):  # pylint: disable=abstract-method
    """Point-at-Infinity abstract base class."""

    @property
    def _short_repr(self) -> str:
        return f'Pt@Inf {self.name}'
