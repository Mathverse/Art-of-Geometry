"""Abstract Space."""


from collections.abc import Sequence
from dataclasses import dataclass

from ._entity import _GeometryEntityABC
from ._point import _ConcretePointABC


__all__: Sequence[str] = ('_SpaceABC',
                          '_SubSpaceABC', '_HalfSpaceABC', '_ClosedSubSpaceABC')  # noqa: E501


class _SpaceABC(_GeometryEntityABC):
    """Abstract Space."""


class _SubSpaceABC(_GeometryEntityABC):
    """Abstract Sub-Space."""


@dataclass
class _HalfSpaceABC(_SubSpaceABC):
    """Abstract Half Space with a specified Boundary and containing a Point."""

    boundary: _SpaceABC
    point: _ConcretePointABC


class _ClosedSubSpaceABC(_SubSpaceABC):
    """Abstract Closed Sub-Space enclosed within Boundary(ies)."""
