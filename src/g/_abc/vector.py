"""Vector.

In this Art of Geometry package, Vectors are considered fundamental, objective
3-DIMENSIONAL geometric entities independent of Spaces and Points.

Each Vector is represented by a definitive triplet of real numbers/variables.

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


from collections.abc import Sequence
from dataclasses import dataclass
from functools import cache
from typing import LiteralString, Self

from sympy.vector.vector import Vector as SymPyVector

from ..variable import RealVarOrNum
from .entity import _GeomEntityABC


__all__: Sequence[LiteralString] = 'Vector', 'Ux', 'Uy', 'Uz'


@dataclass
class Vector(_GeomEntityABC, SymPyVector):
    """(3-Dimensional) Vector."""

    x: RealVarOrNum = 1
    y: RealVarOrNum = 0
    z: RealVarOrNum = 0

    @cache
    def __len__(self: Self) -> RealVarOrNum:
        """Return length/magnitude/modulus."""
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** .5

    @cache
    def unit(self) -> Self:
        """Return unit vector."""
        m: RealVarOrNum = len(self)
        return type(self)(x=self.x / m, y=self.y / m, z=self.z / m)


# global unit vectors
Ux: Vector = Vector(x=1, y=0, z=0)
Uy: Vector = Vector(x=0, y=1, z=0)
Uz: Vector = Vector(x=0, y=0, z=1)
