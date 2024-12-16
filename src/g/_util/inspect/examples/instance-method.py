"""Instance-Method Object Inspection."""


from __future__ import annotations

from inspect import isfunction, ismethod, isroutine
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import is_instance_method, describe

if TYPE_CHECKING:
    from typing import Self


class Cls:
    """A Class."""

    def meth(self: Self) -> None:
        """An Instance Method."""  # noqa: D401


print(f'{Cls.meth} Is Unbound Instance Method? {is_instance_method(Cls.meth, bound=False)}')  # noqa: E501
print(f'{Cls.meth} Is Function? {isfunction(Cls.meth)}')
print(f'{Cls.meth} Is Routine? {isroutine(Cls.meth)}')
pprint(describe(Cls.meth))


inst: Cls = Cls()

print(f'{inst.meth} Is Bound Instance Method? {is_instance_method(inst.meth, bound=True)}')  # noqa: E501
print(f'{inst.meth} Is Bound Instance Method? {ismethod(inst.meth)}')
print(f'{inst.meth} Is Routine? {isroutine(inst.meth)}')
pprint(describe(inst.meth))
