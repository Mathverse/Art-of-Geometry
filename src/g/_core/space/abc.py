"""Abstract Space."""


from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from typing import LiteralString, Self

from sympy.core.expr import Expr

from ..entity.geom import _GeomEntityABC
from ..point.abc import AConcretePoint


__all__: Sequence[LiteralString] = ('_SpaceABC',)


class _SpaceABC(_GeomEntityABC):
    """Abstract Space."""

    @cached_property
    @abstractmethod
    def equation(self: Self, /) -> Expr:
        """Cartesian equation."""
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def parametric_equations(self: Self, /) -> tuple[Expr, ...]:
        """Parametric equations."""
        raise NotImplementedError


class _SubSpaceABC(_GeomEntityABC):
    """Abstract Sub-Space."""


@dataclass
class _HalfSpaceABC(_SubSpaceABC):
    """Abstract Half Space with a specified Boundary and containing a Point."""

    boundary: _SpaceABC
    point: AConcretePoint


class _ClosedSubSpaceABC(_SubSpaceABC):
    """Abstract Closed Sub-Space enclosed within Boundary(ies)."""
