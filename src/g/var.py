__all__ = \
    'Variable', 'Var', \
    'VARIABLE_AND_NUMERIC_TYPES', 'OptionalVariableOrNumericType'


from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from typing import Union

from .._util._tmp import TMP_NAME_FACTORY
from .._util._type import NUMERIC_TYPES, OptionalStrOrCallableReturningStrType, OptionalSymPyExprType, OptionalStrOrSymPyExprType
from ._abc._entity import _EntityABC


class Variable(_EntityABC, Symbol):
    _NAME_NULLABLE = False

    def __new__(
            cls,
            expr_or_name: OptionalStrOrSymPyExprType = None, /,
            *, expr: OptionalSymPyExprType = None, name: OptionalStrOrCallableReturningStrType = None,
            **assumptions: bool) \
            -> Symbol:
        if isinstance(expr_or_name, Expr):
            assert expr is None, \
                '*** EXPR ALREADY GIVEN POSITIONALLY ***'

        elif isinstance(expr_or_name, str):
            assert name is None, \
                '*** NAME ALREADY GIVEN POSITIONALLY ***'

            name = expr_or_name

        if callable(name):
            name = name()
        elif not name:
            name = TMP_NAME_FACTORY()
        cls._validate_name(name)

        return super().__new__(cls, name=name, **assumptions)

    def __init__(
            self,
            expr_or_name: OptionalStrOrSymPyExprType = None, /,
            *, expr: OptionalSymPyExprType = None, name: OptionalStrOrCallableReturningStrType = None,
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
        return f"var {self.name}{f' = {self.expr}' if self.expr else ''}"

    @property
    def free(self) -> bool:
        return self.expr is None


# alias
Var = Variable


# type constants
VARIABLE_AND_NUMERIC_TYPES = (Variable,) + NUMERIC_TYPES
OptionalVariableOrNumericType = Union[VARIABLE_AND_NUMERIC_TYPES + (None,)]
