"""Inspect Class Object."""


from __future__ import annotations

from inspect import isclass
from pprint import pprint

from g._util.inspect import describe


class C:
    """A Class."""


print(f'{C} Is Class? {isclass(C)}')
pprint(describe(C, is_class=True))
