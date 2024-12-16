"""Iterator Object Inspection."""


from __future__ import annotations

from inspect import isgenerator
from pprint import pprint
from typing import TYPE_CHECKING

from g._util.inspect import describe

if TYPE_CHECKING:
    from collections.abc import Iterator


it: Iterator[int] = (i for i in range(0))

print(f'{it} Is Generator? {isgenerator(it)}')
pprint(describe(it))
