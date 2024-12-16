"""Abstract Class Object Inspection."""


from __future__ import annotations

from abc import ABC, abstractmethod
from inspect import isabstract, isclass
from pprint import pprint

from g._util.inspect import describe


class ACls(ABC):
    """An Abstract Base Class."""

    @abstractmethod
    def ab_meth(self) -> None:
        """An Abstract Method."""  # noqa: D401


print(f'{ACls} Is Abstract? {isabstract(ACls)}')
print(f'{ACls} Is Class? {isclass(ACls)}')
pprint(describe(ACls, is_class=True))
