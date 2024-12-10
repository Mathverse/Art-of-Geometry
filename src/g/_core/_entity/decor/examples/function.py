"""Inspect Function."""


from __future__ import annotations

from inspect import isfunction
from pprint import pprint

from g._util.inspect import describe


def f() -> None:
    """A Function."""  # noqa: D401


print(f'{f} Is Function? {isfunction(f)}')
pprint(describe(f))
