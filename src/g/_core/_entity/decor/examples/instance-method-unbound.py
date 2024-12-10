"""Inspect Unbound Instance Method."""


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


print(f'{C.m} Is Function? {isfunction(C.m)}')
print(f'{C.m} Is Bound Instance Method? {ismethod(C.m)}')
print(f'{C.m} Is Bound Instance Method? {is_instance_method(C.m, bound=True)}')
print(f'{C.m} Is Unbound Instance Method? {is_instance_method(C.m, bound=False)}')  # noqa: E501
pprint(describe(C.m))
