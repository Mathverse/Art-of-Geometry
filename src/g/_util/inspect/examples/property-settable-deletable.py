"""Settable-&-Deletable-Property Object Inspection."""


from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import (is_property, is_settable_property,
                             is_settable_deletable_property, describe)

if TYPE_CHECKING:
    from typing import Self


class Cls:
    """A Class."""

    @property
    def pty(self: Self) -> int:
        """Get Property Value."""
        return self._p

    @pty.setter
    def pty(self: Self, v: int) -> None:
        """Set Property Value."""
        self._p: int = v

    @pty.deleter
    def pty(self: Self) -> None:
        """Set Property Value to 0."""
        self._p: int = 0


print(f'{Cls.pty} Is Settable & Deletable Property? {is_settable_deletable_property(Cls.pty)}')  # noqa: E501
print(f'{Cls.pty} Is Settable Property? {is_settable_property(Cls.pty)}')
print(f'{Cls.pty} Is Property? {is_property(Cls.pty)}')
pprint(describe(Cls.pty))
