"""Property Object Inspection."""


from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import is_property, describe

if TYPE_CHECKING:
    from typing import Self


class Cls:
    """A Class."""

    @property
    def pty(self: Self) -> None:
        """A Property."""


print(f'{Cls.pty} Is Property? {is_property(Cls.pty)}')
pprint(describe(Cls.pty))
