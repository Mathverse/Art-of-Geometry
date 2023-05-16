"""Algebra Backends."""


from collections.abc import Sequence
from typing import LiteralString

from .sympy import SymPyBackend


__all__: Sequence[LiteralString] = ('SymPyBackend',)
