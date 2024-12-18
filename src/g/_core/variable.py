"""Variable.

Variables are non-geometric entities representing numbers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.core.expr import Expr
from sympy.core.symbol import Symbol

from g._util.type import (Num, RealNum,
                          OptionalStrOrCallableReturningStr,
                          OptionalSymPyExpr, OptionalStrOrSymPyExpr)
from g._util.unique_name import UNIQUE_NAME_FACTORY

from ._entity import ANonGeomEntity, assign_entity_dependencies_and_name

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self


__all__: Sequence[LiteralString] = ('Variable', 'Var',
                                    'RealVariable', 'RealVar',
                                    'NumOrVar', 'OptionalNumOrVar',
                                    'RealNumOrVar', 'OptionalRealNumOrVar')


@assign_entity_dependencies_and_name
class Variable(ANonGeomEntity, Symbol):
    """Variable."""

    _NAME_NULLABLE: bool = False

    def __new__(cls: type,
                expr_or_name: OptionalStrOrSymPyExpr = None, /, *,
                expr: OptionalSymPyExpr = None,
                name: OptionalStrOrCallableReturningStr = None,
                **assumptions: bool) -> Symbol:
        """Create new variable."""
        # validate arguments
        if isinstance(expr_or_name, Expr):
            assert expr is None, \
                TypeError('*** EXPR ALREADY GIVEN POSITIONALLY ***')

        elif isinstance(expr_or_name, str):
            assert name is None, \
                TypeError('*** NAME ALREADY GIVEN POSITIONALLY ***')

            name: str = expr_or_name

        # generate name if not already given as string
        if callable(name):
            name: str = name()
        elif not name:
            name: str = UNIQUE_NAME_FACTORY()

        # validate name
        cls._validate_name(name)

        # create variable
        return super().__new__(cls, name=name, **assumptions)

    def __init__(self: Self,
                 expr_or_name: OptionalStrOrSymPyExpr = None, /, *,
                 expr: OptionalSymPyExpr = None,
                 name: OptionalStrOrCallableReturningStr = None,
                 **assumptions: bool) -> None:  # noqa: ARG002
        """Initialize variable."""
        if isinstance(expr_or_name, Expr):
            assert expr is None, \
                TypeError('*** EXPR ALREADY GIVEN POSITIONALLY ***')

            expr: Expr = expr_or_name

        elif isinstance(expr_or_name, str):
            assert name is None, \
                TypeError('*** NAME ALREADY GIVEN POSITIONALLY ***')

        self.expr: Expr = expr

    @property
    def _short_repr(self: Self, /) -> str:
        """Return short string representation."""
        return f"var {self.name}{f' = {self.expr}' if self.expr else ''}"

    @property
    def free(self: Self, /) -> bool:
        """Check if variable is free."""
        return self.expr is None


# alias
Var = Variable


class RealVariable(Variable):
    """Real-valued Variable."""


# alias
RealVar = RealVariable


# type constants
NumOrVar: type = Num | Var
OptionalNumOrVar: type = NumOrVar | None

RealNumOrVar: type = RealNum | RealVar
OptionalRealNumOrVar: type = RealNumOrVar | None
