"""Abstract Algebra Backend."""


from abc import ABC
from collections.abc import Sequence
from typing import LiteralString


__all__: Sequence[LiteralString] = ('_AlgBackendABC',)


class _AlgBackendABC(ABC):
    """Abstract Algebra Backend."""
