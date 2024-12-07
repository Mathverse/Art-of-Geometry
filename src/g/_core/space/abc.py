"""Abstract Space classes."""


from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

from sympy.core.expr import Expr

from .._entity import AGeomEntity
from ..point import AConcretePoint

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self


__all__: Sequence[LiteralString] = ('ASpace',
                                    'ASubSpace', 'AHalfSpace', 'AClosedSubSpace')  # noqa: E501


class ASpace(AGeomEntity):
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


class ASubSpace(AGeomEntity):
    """Abstract Sub-Space."""


@dataclass
class AHalfSpace(ASubSpace):
    """Abstract Half Space with a specified Boundary and containing a Point."""

    boundary: ASpace
    point: AConcretePoint


class AClosedSubSpace(ASubSpace):
    """Abstract Closed Sub-Space enclosed within Boundary(ies)."""
