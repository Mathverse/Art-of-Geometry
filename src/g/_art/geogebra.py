"""Geogebra Art Frontend."""


from collections.abc import Sequence
from typing import LiteralString

from .abc import _ArtFrontendABC


__all__: Sequence[LiteralString] = ('GeogebraFrontend',)


class GeogebraFrontend(_ArtFrontendABC):
    """Geogebra Art Frontend."""
