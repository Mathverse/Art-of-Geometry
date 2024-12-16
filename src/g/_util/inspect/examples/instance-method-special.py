"""Inspect Unbound Instance Method."""


from __future__ import annotations

from inspect import isfunction, ismethod
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import is_instance_method, describe

if TYPE_CHECKING:
    from typing import Self


class Cls:
    """A Class."""

    def meth(self: Self) -> None:
        """An Instance Method."""  # noqa: D401


pprint(describe(Cls.meth))
