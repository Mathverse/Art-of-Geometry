"""Abstract Coordinate System."""


from abc import abstractmethod
from collections.abc import Sequence
from typing import LiteralString

from ..variable import RealVarOrNum

from .point import _PointABC
from .space.abc import _SpaceABC


__all__: Sequence[LiteralString] = ('_CoordinateSystemABC',)


class _CoordinateSystemABC:
    """Abstract Coordinate System."""

    @abstractmethod
    def __call__(self, point: _PointABC, space: _SpaceABC) -> tuple[RealVarOrNum]:  # noqa: E501
        """Return coordinate of Point in Space."""
        raise NotImplementedError
