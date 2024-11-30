"""Cyclic Tuple."""


from collections.abc import Sequence
from functools import cached_property
from typing import Any, LiteralString, Self


__all__: Sequence[LiteralString] = ('CyclicTuple',)


class CyclicTuple(tuple):
    """Cyclic Tuple."""

    @cached_property
    def len(self: Self, /) -> int:
        """Return length."""
        return len(self)

    def __getitem__(self: Self, n: int, /) -> Any:
        """Return item number n."""
        return self[n % self.len]
