"""SymPy Algebra Backend."""


from collections.abc import Sequence
from typing import LiteralString

from .abc import _AlgBackendABC


__all__: Sequence[LiteralString] = ('SymPyBackend',)


class SymPyBackend(_AlgBackendABC):
    """SymPy Algebra Backend."""
