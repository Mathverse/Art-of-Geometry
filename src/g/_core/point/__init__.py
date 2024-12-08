"""Point classes."""


from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import APoint, AConcretePoint, APointAtInf
from .euclid import EuclidPoint, EuclidConcretePoint, EuclidPointAtInf, EUCLID_ORIG  # noqa: E501

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = (
    'APoint', 'AConcretePoint', 'APointAtInf',
    'EuclidPoint', 'EuclidConcretePoint', 'EuclidPointAtInf', 'EUCLID_ORIG',
    'Point', 'Pt', 'PointAtInf', 'PtAtInf', 'ORIG',
)


# aliases
Point = Pt = EuclidConcretePoint
PointAtInf = PtAtInf = EuclidPointAtInf
ORIG: EuclidConcretePoint = EUCLID_ORIG
