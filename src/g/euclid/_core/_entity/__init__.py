"""Euclidean Geometric Entity classes."""


from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import AnEuclidGeomEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('AnEuclidGeomEntity',)
