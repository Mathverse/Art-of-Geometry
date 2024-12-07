"""Abstract Space classes."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from typing import LiteralString, Self

from sympy.core.expr import Expr

from .._entity.geom import _GeomEntityABC
from ..point.abc import AConcretePoint


__all__: Sequence[LiteralString] = ('ASpace',
                                    'ASubSpace', 'AHalfSpace', 'AClosedSubSpace')  # noqa: E501


class ASpace(_GeomEntityABC):
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


class ASubSpace(_GeomEntityABC):
    """Abstract Sub-Space."""


@dataclass
class AHalfSpace(ASubSpace):
    """Abstract Half Space with a specified Boundary and containing a Point."""

    boundary: ASpace
    point: AConcretePoint


class AClosedSubSpace(ASubSpace):
    """Abstract Closed Sub-Space enclosed within Boundary(ies)."""
