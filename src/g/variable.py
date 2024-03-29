"""Variable."""


from collections.abc import Sequence
from typing import LiteralString, Optional, Self

from sympy.core.expr import Expr
from sympy.core.symbol import Symbol

from ._abc.entity.abc import _EntityABC

from ._util.type import (Num, OptionalStrOrCallableReturningStr,
                         OptionalSymPyExpr, OptionalStrOrSymPyExpr)
from ._util.unique_name import UNIQUE_NAME_FACTORY


__all__: Sequence[LiteralString] = ('Variable', 'Var',
                                    'VarOrNum', 'OptionalVarOrNum')


class Variable(_EntityABC, Symbol):
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
                 **assumptions: bool) -> None:
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


# type constants
VarOrNum: type = Var | Num
OptionalVarOrNum: type = Optional[VarOrNum]
