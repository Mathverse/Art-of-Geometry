"""Variables."""


from collections.abc import Sequence
from typing import Optional

from sympy.core.expr import Expr
from sympy.core.symbol import Symbol

from .._util.tmp import TMP_NAME_FACTORY
from .._util.type import (Num, OptionalStrOrCallableReturningStr,
                          OptionalSymPyExpr, OptionalStrOrSymPyExpr)
from ._abc._entity import _EntityABC


__all__: Sequence[str] = ('Variable', 'Var',
                          'VarOrNum', 'OptionalVarOrNum')


class Variable(_EntityABC, Symbol):
    """Variable."""

    _NAME_NULLABLE = False

    def __new__(cls,
                expr_or_name: OptionalStrOrSymPyExpr = None, /, *,
                expr: OptionalSymPyExpr = None,
                name: OptionalStrOrCallableReturningStr = None,
                **assumptions: bool) -> Symbol:
        """Create new variable."""
        if isinstance(expr_or_name, Expr):
            assert expr is None, '*** EXPR ALREADY GIVEN POSITIONALLY ***'

        elif isinstance(expr_or_name, str):
            assert name is None, '*** NAME ALREADY GIVEN POSITIONALLY ***'

            name = expr_or_name

        if callable(name):
            name = name()
        elif not name:
            name = TMP_NAME_FACTORY()
        cls._validate_name(name)

        return super().__new__(cls, name=name, **assumptions)

    def __init__(self,
                 expr_or_name: OptionalStrOrSymPyExpr = None, /, *,
                 expr: OptionalSymPyExpr = None,
                 name: OptionalStrOrCallableReturningStr = None,
                 **assumptions: bool) -> None:
        """Initialize variable."""
        if isinstance(expr_or_name, Expr):
            assert expr is None, '*** EXPR ALREADY GIVEN POSITIONALLY ***'

            expr = expr_or_name

        elif isinstance(expr_or_name, str):
            assert name is None,  '*** NAME ALREADY GIVEN POSITIONALLY ***'

        self.expr = expr

    @property
    def _short_repr(self) -> str:
        """Return short string representation."""
        return f"var {self.name}{f' = {self.expr}' if self.expr else ''}"

    @property
    def free(self) -> bool:
        """Check if variable is free."""
        return self.expr is None


# alias
Var = Variable


# type constants
VarOrNum: type = Var | Num
OptionalVarOrNum: type = Optional[VarOrNum]
