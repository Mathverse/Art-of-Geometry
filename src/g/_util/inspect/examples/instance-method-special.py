"""Instance-Special-Operator Object Inspection."""


from __future__ import annotations

from inspect import isfunction, ismethod, isroutine
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import (is_instance_method, is_instance_special_operator,
                             describe)

if TYPE_CHECKING:
    from typing import Self


class Cls:
    """A Class."""

    def __op__(self: Self) -> None:
        """An Special Instance Operator."""  # noqa: D401


print(f'{Cls.__op__} Is Unbound Instance Special Operator?'
      f' {is_instance_special_operator(Cls.__op__, bound=False)}')
print(f'{Cls.__op__} Is Unbound Instance Method? {is_instance_method(Cls.__op__, bound=False)}')  # noqa: E501
print(f'{Cls.__op__} Is Function? {isfunction(Cls.__op__)}')
print(f'{Cls.__op__} Is Routine? {isroutine(Cls.__op__)}')
pprint(describe(Cls.__op__))


inst: Cls = Cls()

print(f'{inst.__op__} Is Bound Instance Special Operator?'
      f' {is_instance_special_operator(inst.__op__, bound=True)}')
print(f'{inst.__op__} Is Bound Instance Method? {is_instance_method(inst.__op__, bound=True)}')  # noqa: E501
print(f'{inst.__op__} Is Bound Instance Method? {ismethod(inst.__op__)}')
print(f'{inst.__op__} Is Routine? {isroutine(inst.__op__)}')
pprint(describe(inst.__op__))
