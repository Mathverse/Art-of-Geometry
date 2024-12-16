"""Instance-Method Object Inspection."""


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


print(f'{Cls.meth} Is Function? {isfunction(Cls.meth)}')
print(f'{Cls.meth} Is Bound Instance Method? {ismethod(Cls.meth)}')
print(f'{Cls.meth} Is Bound Instance Method? {is_instance_method(Cls.meth, bound=True)}')  # noqa: E501
print(f'{Cls.meth} Is Unbound Instance Method? {is_instance_method(Cls.meth, bound=False)}')  # noqa: E501


inst: Cls = Cls()

print(f'{inst.meth} Is Function? {isfunction(inst.meth)}')
print(f'{inst.meth} Is Bound Instance Method? {ismethod(inst.meth)}')
print(f'{inst.meth} Is Bound Instance Method? {is_instance_method(inst.meth, bound=True)}')  # noqa: E501
print(f'{inst.meth} Is Unbound Instance Method? {is_instance_method(inst.meth, bound=False)}')  # noqa: E501
pprint(describe(inst.meth))
