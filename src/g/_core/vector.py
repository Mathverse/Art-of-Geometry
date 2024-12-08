"""Vector.

In this Art of Geometry package, Vectors are considered fundamental, objective
3-DIMENSIONAL NON-GEOMETRIC entities independent of geometric Spaces & Points.

Each Vector is represented by a definitive triplet of real-valued numbers or
variables.

3 unit vectors named Ux, Uy & Uz are instantiated to represent our global/usual
3-dimensional Euclidean orthogonal spatial directions.

Spaces and their corresponding coordinate systems shall be characterized by
their various relevant vectors, e.g., basis and direction/orientation vectors.

Points' coordinates (e.g., cartesian, polar, etc.) relative to the Spaces
containing such Points shall be defined and/or derived based on such Spaces'
characteristic vectors.

The Lebesgue measures of Euclidean Subspaces (e.g., linear segment lengths,
planar shape areas, 3-dimensional solid volumes, etc.) shall also be defined
and/or derived based on such Subspaces' corresponding containing Spaces'
characteristic vectors.
"""


from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING

from ._entity import ANonGeomEntity
from .variable import RealNumOrVar

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self


__all__: Sequence[LiteralString] = ('Vector', 'Vec', 'V',
                                    'OptionalVec',
                                    'Ux', 'Uy', 'Uz', 'V0')


@dataclass
class Vector(ANonGeomEntity):
    """(3-Dimensional) Vector."""

    x: RealNumOrVar = 0
    y: RealNumOrVar = 0
    z: RealNumOrVar = 0

    @cache
    def __len__(self: Self) -> RealNumOrVar:
        """Return length/magnitude/modulus."""
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** .5

    @cache
    def unit(self) -> Self:
        """Return unit vector."""
        m: RealNumOrVar = len(self)
        return type(self)(x=self.x / m, y=self.y / m, z=self.z / m)


# aliases
V = Vec = Vector


# type constants
OptionalVec: type = Vec | None


# global unit vectors
Ux: V = V(x=1)
Uy: V = V(y=1)
Uz: V = V(z=1)

# zero vector
V0: V = V()
