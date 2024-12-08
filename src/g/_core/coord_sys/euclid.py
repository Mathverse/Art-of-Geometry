"""(Absolute/Global/Standard) Euclidean Coordinate System."""


from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict, TYPE_CHECKING

from .abc import ACoordSys

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self, NotRequired

    from ..point import APoint
    from ..variable import RealNumOrVar, OptionalRealNumOrVar
    from ..vector import OptionalVec


__all__: Sequence[LiteralString] = ('EuclidCoords',
                                    'EuclidCoordSys', 'EUCLID_COORD_SYS')


class EuclidCoordDict(TypedDict):
    x: NotRequired[OptionalRealNumOrVar]
    y: NotRequired[OptionalRealNumOrVar]
    z: NotRequired[OptionalRealNumOrVar]
    inf_dir: NotRequired[OptionalVec]


@dataclass
class EuclidCoords:
    x: OptionalRealNumOrVar = None
    y: OptionalRealNumOrVar = None
    z: OptionalRealNumOrVar = None
    inf_dir: OptionalVec = None


EUCLID_COORD_SYS_NAME: LiteralString = 'EUCLID_COORD_SYS'


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=True,  # force hashing using unique name
           frozen=True,  # TODO: decide whether immutability is necessary
           match_args=True,
           kw_only=False,
           slots=False,
           weakref_slot=False)
class EuclidCoordSys(ACoordSys):
    """(Absolute/Global/Standard) Euclidean Coordinate System."""

    name: str = EUCLID_COORD_SYS_NAME

    def __call__(self: Self, *coords: RealNumOrVar, **kw_coords: EuclidCoordDict) -> APoint:  # noqa: E501
        """Return Point from coordinates."""
        raise NotImplementedError

    def locate(self: Self, point: APoint) -> EuclidCoords:
        return point.coords[self]


# Default Absolute/Global/Standard Euclidean Coordinate System
EUCLID_COORD_SYS: EuclidCoordSys = EuclidCoordSys()
