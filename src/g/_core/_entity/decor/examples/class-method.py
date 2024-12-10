"""Class-Method Object Inspection."""


from __future__ import annotations

from inspect import ismethod
from pprint import pprint

from g._util.inspect import is_class_method, describe


class Cls:
    """A Class."""

    @classmethod
    def cls_method(cls) -> None:
        """A Class Method."""  # noqa: D401


print(f'{Cls.cls_method} Is Method? {ismethod(Cls.cls_method)}')
print(f'{Cls.cls_method} Is Class Method? {is_class_method(Cls.cls_method)}')
pprint(describe(Cls.cls_method))


inst: Cls = Cls()

print(f'{inst.cls_method} Is Method? {ismethod(inst.cls_method)}')
print(f'{inst.cls_method} Is Class Method? {is_class_method(inst.cls_method)}')
pprint(describe(inst.cls_method))
