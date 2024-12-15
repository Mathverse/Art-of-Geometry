"""Inspect Property."""


from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import (is_property, is_settable_property,
                             is_settable_deletable_property, describe)

if TYPE_CHECKING:
    from typing import Self


class C:
    """A Class."""

    @property
    def p(self: Self) -> None:
        """A Property."""


print(f'{C.p} Is Property? {is_property(C.p)}')
print(f'{C.p} Is Settable Property? {is_settable_property(C.p)}')
print(f'{C.p} Is Settable & Deletable Property? {is_settable_deletable_property(C.p)}')  # noqa: E501
pprint(describe(C.p))