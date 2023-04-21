__all__ = '_SpaceABC', '_HalfSpaceABC'


from dataclasses import dataclass

from ._entity import _GeometryEntityABC
from ._point import _ConcretePointABC


class _SpaceABC(_GeometryEntityABC):
    """Abstract Space."""


class _SubSpaceABC(_GeometryEntityABC):
    """Abstract Sub-Space."""


@dataclass
class _HalfSpaceABC(_SubSpaceABC):
    """Abstract Half Space with a specified Boundary and containing a Point."""

    boundary: _SpaceABC
    point: _ConcretePointABC
