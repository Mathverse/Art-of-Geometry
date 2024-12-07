"""Abstract Linear Entities."""


from __future__ import annotations

from typing import TYPE_CHECKING

from .._entity import AGeomEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('ALinearEntity',
                                    'AConcreteLinearEntity',
                                    'ALinearEntityAtInf',

                                    'ALine',

                                    'AConcreteLine',
                                    'AConcreteDirectedLine',

                                    'ALineAtInf',
                                    'ADirectedLineAtInf')


class ALinearEntity(AGeomEntity):
    """Abstract Linear Entity."""


class AConcreteLinearEntity(ALinearEntity):
    """Abstract Concrete Linear Entity."""


class ALinearEntityAtInf(ALinearEntity):
    """Abstract Linear Entity at Infinity."""


class ALine(ALinearEntity):
    """Abstract Line."""


class AConcreteLine(ALine, AConcreteLinearEntity):
    """Abstract Concrete Line."""

    @property
    def name(self) -> str:
        """Name."""
        return (self._name
                if self._name
                else f'-{self.point_0.name}--{self.point_1.name}-')

    @property
    def _short_repr(self) -> str:
        """Short string representation."""
        return f'Ln {self.name}'


class AConcreteDirectedLine(AConcreteLine):
    """Abstract Concrete Directed Line."""

    @property
    def name(self) -> str:
        """Name."""
        return (self._name
                if self._name
                else f'-{self.point_0.name}->{self.point_1.name}-')

    @property
    def _short_repr(self) -> str:
        """Short string representation."""
        return f'DirLn {self.name}'


class ALineAtInf(ALine, ALinearEntityAtInf):
    """Abstract Line at Infinity."""


class ADirectedLineAtInf(ALineAtInf):
    """Abstract Directed Line at Infinity."""
