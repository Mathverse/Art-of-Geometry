"""Inspect Bound Instance Method."""


from __future__ import annotations

from inspect import isfunction, ismethod
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import is_instance_method, describe

if TYPE_CHECKING:
    from typing import Self


class C:
    """A Class."""

    def m(self: Self) -> None:
        """An Instance Method."""  # noqa: D401


i: C = C()


print(f'{i.m} Is Function? {isfunction(i.m)}')
print(f'{i.m} Is Bound Instance Method? {ismethod(i.m)}')
print(f'{i.m} Is Bound Instance Method? {is_instance_method(i.m, bound=True)}')
print(f'{i.m} Is Unbound Instance Method? {is_instance_method(i.m, bound=False)}')  # noqa: E501
pprint(describe(i.m))
