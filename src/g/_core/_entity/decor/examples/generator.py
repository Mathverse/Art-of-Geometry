"""Generator Object Inspection."""


from collections.abc import Generator
from inspect import isgenerator


gen: Generator[int, None, None] = (i for i in range(0))  # noqa: UP043

print(f'{gen} Is Generator? {isgenerator(gen)}')
