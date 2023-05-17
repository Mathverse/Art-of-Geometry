"""Art Frontends."""


from collections.abc import Sequence
from typing import LiteralString

from .manim import MAnimFrontend


__all__: Sequence[LiteralString] = ('MAnimFrontend',)
