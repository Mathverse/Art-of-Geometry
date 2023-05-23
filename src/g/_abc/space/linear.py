"""Abstract Linear Entities."""


from __future__ import annotations

from collections.abc import Sequence
from typing import LiteralString


__all__: Sequence[LiteralString] = (
    '_LinearEntityABC',
    '_ConcreteLinearEntityABC',
    '_LinearEntityAtInfinityABC',

    '_LineABC',

    '_ConcreteLineABC',
    '_ConcreteDirectedLineABC',

    '_LineAtInfinityABC',
    '_DirectedLineAtInfinityABC',
)


from ._entity import _GeomEntityABC


class _LinearEntityABC(_GeomEntityABC):
    pass


class _ConcreteLinearEntityABC(_LinearEntityABC):
    pass


class _LinearEntityAtInfinityABC(_LinearEntityABC):
    pass


class _LineABC(_LinearEntityABC):
    pass


class _ConcreteLineABC(_LineABC, _ConcreteLinearEntityABC):
    @property
    def name(self) -> str:
        return (self._name
                if self._name
                else f'-{self.point_0.name}--{self.point_1.name}-')

    @property
    def _short_repr(self) -> str:
        return f'Ln {self.name}'


class _ConcreteDirectedLineABC(_ConcreteLineABC):
    @property
    def name(self) -> str:
        return (self._name
                if self._name
                else f'-{self.point_0.name}->{self.point_1.name}-')

    @property
    def _short_repr(self) -> str:
        return f'DirLn {self.name}'


class _LineAtInfinityABC(_LineABC, _LinearEntityAtInfinityABC):
    pass


class _DirectedLineAtInfinityABC(_LineAtInfinityABC):
    pass
