"""Abstract Vector base class.

In this Art of Geometry package, Vectors are considered fundamental, OBJECTIVE
geometric entities independent of Spaces and Points.

Each Vector has a direction, represented by a definitive tuple of real numbers
whose squares sum to 1, and a magnitude, represented by another real number.

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
from typing import LiteralString

from .._util.type import RealNum
from .entity import _GeomEntityABC


__all__: Sequence[LiteralString] = ('_VectorABC',)


@dataclass
class _VectorABC(_GeomEntityABC):
    """Abstract Vector."""

    direction_unit_components: tuple[RealNum]

    magnitude: RealNum
