"""Class-Method Object Inspection."""


from __future__ import annotations

from inspect import ismethod, isroutine
from pprint import pprint

from g._util.inspect import is_class_method, describe


class Cls:
    """A Class."""

    @classmethod
    def cls_meth(cls) -> None:
        """A Class Method."""  # noqa: D401


print(f'{Cls.cls_meth} Is Class Method? {is_class_method(Cls.cls_meth)}')
print(f'{Cls.cls_meth} Is Method? {ismethod(Cls.cls_meth)}')
print(f'{Cls.cls_meth} Is Routine? {isroutine(Cls.cls_meth)}')
pprint(describe(Cls.cls_meth))


inst: Cls = Cls()

print(f'{inst.cls_meth} Is Class Method? {is_class_method(inst.cls_meth)}')
print(f'{inst.cls_meth} Is Method? {ismethod(inst.cls_meth)}')
print(f'{inst.cls_meth} Is Routine? {isroutine(inst.cls_meth)}')
pprint(describe(inst.cls_meth))
