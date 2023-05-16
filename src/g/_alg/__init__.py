"""Algebra Backends."""


from collections.abc import Sequence
from typing import Literal, LiteralString


__all__: Sequence[LiteralString] = ('AlgebraBackendStr',)


AlgebraBackendStr: type = Literal['SymPy']
