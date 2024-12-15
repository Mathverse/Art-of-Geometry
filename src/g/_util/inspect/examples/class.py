"""Class Object Inspection."""


from __future__ import annotations

from inspect import isclass
from pprint import pprint

from g._util.inspect import describe


class Cls:
    """A Class."""


print(f'{Cls} Is Class? {isclass(Cls)}')
pprint(describe(Cls, is_class=True))
