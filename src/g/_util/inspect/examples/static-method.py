"""Static-Method Object Inspection."""


from __future__ import annotations

from pprint import pprint

from g._util.inspect import is_static_method, describe


class Cls:
    """A Class."""

    @staticmethod
    def stat_meth() -> None:
        """A Static Method."""  # noqa: D401


print(f'{Cls.stat_meth} Is Static Method? {is_static_method(Cls.stat_meth)}')
pprint(describe(Cls.stat_meth))


inst: Cls = Cls()

print(f'{inst.stat_meth} Is Static Method? {is_static_method(inst.stat_meth)}')
pprint(describe(inst.stat_meth))
