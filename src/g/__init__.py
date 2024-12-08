"""Art of Geometry package."""


from __future__ import annotations

from importlib.metadata import version
from typing import TYPE_CHECKING

from ._core import (
    EuclidCoordSys, EUCLID_COORD_SYS,

    EuclidPoint, EuclidConcretePoint, EuclidPointAtInf, EUCLID_ORIG,
    Point, Pt, PointAtInf, PtAtInf, ORIG,

    Variable, Var,

    Vector, Vec, V, Ux, Uy, Uz, V0,
)

from .session import Session, DEFAULT_SESSION

from ._util.cyclic_tuple import CyclicTuple
from ._util import debug

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = (
    '__version__',

    'Session', 'DEFAULT_SESSION',

    'EuclidCoordSys', 'EUCLID_COORD_SYS',

    'EuclidPoint', 'EuclidConcretePoint', 'EuclidPointAtInf', 'EUCLID_ORIG',
    'Point', 'Pt', 'PointAtInf', 'PtAtInf', 'ORIG',

    'Variable', 'Var',

    'Vector', 'Vec', 'V', 'Ux', 'Uy', 'Uz', 'V0',

    'CyclicTuple',

    'debug',
)


__version__: LiteralString = version(distribution_name='Art-of-Geometry')
