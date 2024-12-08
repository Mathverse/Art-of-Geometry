"""Euclidean Point classes."""


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sympy.core.numbers import oo

from .abc import APoint, AConcretePoint, APointAtInf

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString

    from ..variable import RealNumOrVar, OptionalRealNumOrVar
    from ..vector import Vec, OptionalVec


__all__: Sequence[LiteralString] = ('EuclidPoint',
                                    'EuclidConcretePoint', 'EuclidPointAtInf',
                                    'EUCLID_ORIG')


@dataclass
class EuclidPoint(APoint):
    """Euclidean Point."""

    x: OptionalRealNumOrVar = 0
    y: OptionalRealNumOrVar = 0
    z: OptionalRealNumOrVar = 0

    inf_dir: OptionalVec = None


@dataclass
class EuclidConcretePoint(EuclidPoint, AConcretePoint):
    """Euclidean Concrete Point."""

    x: RealNumOrVar = 0
    y: RealNumOrVar = 0
    z: RealNumOrVar = 0

    inf_dir: OptionalVec = None


@dataclass
class EuclidPointAtInf(EuclidPoint, APointAtInf):
    """Euclidean Point at Infinity."""

    inf_dir: Vec

    x: RealNumOrVar = oo
    y: RealNumOrVar = oo
    z: RealNumOrVar = oo


# origin
EUCLID_ORIG: EuclidConcretePoint = EuclidConcretePoint()
