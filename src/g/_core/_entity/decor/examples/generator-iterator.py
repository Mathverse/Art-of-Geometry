"""Iterator Object Inspection."""


from __future__ import annotations

from inspect import isgenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


it: Iterator[int] = (i for i in range(0))

print(f'{it} Is Generator? {isgenerator(it)}')
