"""Generator Object Inspection."""


from __future__ import annotations

from inspect import isgenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


gen: Generator[int, None, None] = (i for i in range(0))  # noqa: UP043

print(f'{gen} Is Generator? {isgenerator(gen)}')
