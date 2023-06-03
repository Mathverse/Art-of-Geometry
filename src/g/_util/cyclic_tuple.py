"""Cyclic Sequence."""


from collections.abc import Sequence
from typing import Any, LiteralString, Self


__all__: Sequence[LiteralString] = ('CyclicTuple',)


class CyclicTuple(tuple):
    """Cyclic Tuple."""

    def __getitem__(self: Self, n: int, /) -> Any:
        """Return item number n."""
        return self[n % len(self)]
