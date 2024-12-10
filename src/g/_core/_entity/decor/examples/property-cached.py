"""Inspect Cached Property."""


from __future__ import annotations

from functools import cached_property
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import is_cached_property, describe

if TYPE_CHECKING:
    from typing import Self


class C:
    """A Class."""

    @cached_property
    def cp(self: Self) -> None:
        """A Cached Property."""


print(f'{C.cp} Is Cached Property? {is_cached_property(C.cp)}')
pprint(describe(C.cp))
