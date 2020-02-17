__all__ = \
    'Variable', 'Var', \
    'VARIABLE_AND_NUMERIC_TYPES', 'OptionalVariableOrNumericType'


from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from typing import Union
from uuid import uuid4

from ..util.types import NUMERIC_TYPES, OptionalStrType, OptionalSymPyExprType, OptionalStrOrSymPyExprType
from .abc import _EntityABC


class Variable(_EntityABC, Symbol):
    def __new__(
            cls,
            expr_or_name: OptionalStrOrSymPyExprType = None, /,
            *, expr: OptionalSymPyExprType = None, name: OptionalStrType = None,
            **assumptions: bool) \
            -> Symbol:
        if isinstance(expr_or_name, Expr):
            assert expr is None, \
                '*** EXPR ALREADY GIVEN POSITIONALLY ***'

        elif isinstance(expr_or_name, str):
            assert name is None, \
                '*** NAME ALREADY GIVEN POSITIONALLY ***'

            name = expr_or_name

        return super().__new__(
                cls,
                name=name
                    if isinstance(name, str) and name
                    else str(uuid4()),
                **assumptions)

    def __init__(
            self,
            expr_or_name: OptionalStrOrSymPyExprType = None, /,
            *, expr: OptionalSymPyExprType = None, name: OptionalStrType = None,
            **assumptions: bool) \
            -> None:
        if isinstance(expr_or_name, Expr):
            assert expr is None, \
                '*** EXPR ALREADY GIVEN POSITIONALLY ***'

            expr = expr_or_name

        elif isinstance(expr_or_name, str):
            assert name is None, \
                '*** NAME ALREADY GIVEN POSITIONALLY ***'

        self.expr = expr

    @property
    def _short_repr(self) -> str:
        return f"Var {self.name}{f' = {self.expr}' if self.expr else ''}"

    @property
    def free(self):
        return self.expr is None


# alias
Var = Variable


# type constants
VARIABLE_AND_NUMERIC_TYPES = (Variable,) + NUMERIC_TYPES
OptionalVariableOrNumericType = Union[VARIABLE_AND_NUMERIC_TYPES + (None,)]
