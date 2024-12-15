"""Cached-Property Object Inspection."""


from __future__ import annotations

from functools import cached_property
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import is_cached_property, describe

if TYPE_CHECKING:
    from typing import Self


class Cls:
    """A Class."""

    @cached_property
    def cached_pty(self: Self) -> None:
        """A Cached Property."""


print(f'{Cls.cached_pty} Is Cached Property? {is_cached_property(Cls.cached_pty)}')  # noqa: E501
pprint(describe(Cls.cached_pty))
