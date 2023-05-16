"""MAnim Art Frontend."""


from collections.abc import Sequence
from typing import LiteralString

from .abc import _ArtFrontendABC


__all__: Sequence[LiteralString] = ('MAnimFrontend',)


class MAnimFrontend(_ArtFrontendABC):
    """MAnim Art Frontend."""
