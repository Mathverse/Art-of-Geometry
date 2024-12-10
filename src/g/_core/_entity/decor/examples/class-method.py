"""Inspect Class Method."""


from __future__ import annotations

from inspect import ismethod
from pprint import pprint

from g._util.inspect import is_class_method, describe


class C:
    """A Class."""

    @classmethod
    def m(cls) -> None:
        """A Class Method."""  # noqa: D401


print(f'{C.m} Is Method? {ismethod(C.m)}')
print(f'{C.m} Is Class Method? {is_class_method(C.m)}')
pprint(describe(C.m))
