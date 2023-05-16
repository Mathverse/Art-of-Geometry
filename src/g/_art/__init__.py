"""Art Frontends."""


from collections.abc import Sequence
from typing import LiteralString

from .abc import _ArtFrontendABC
from .manim import MAnimFrontend


__all__: Sequence[LiteralString] = '_ArtFrontendABC', 'MAnimFrontend'
