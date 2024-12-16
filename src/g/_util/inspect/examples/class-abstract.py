"""Abstract Class Object Inspection."""


from __future__ import annotations

from abc import ABC, abstractmethod
from inspect import isabstract, isclass
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import describe

if TYPE_CHECKING:
    from typing import Self


class ACls(ABC):
    """An Abstract Base Class."""

    @abstractmethod
    def ab_meth(self: Self) -> None:
        """An Abstract Method."""  # noqa: D401


print(f'{ACls} Is Abstract Class? {isabstract(ACls)}')
print(f'{ACls} Is Class? {isclass(ACls)}')
pprint(describe(ACls, is_class=True))
