__all__ = 'Variable', 'Var'


from sympy.core.symbol import Symbol
from typing import Optional
from uuid import uuid4

from ..util.types import OptionalStrType, OptionalSymPyExprType
from .abc import _EntityABC


class Variable(_EntityABC, Symbol):
    def __new__(
            cls,
            name: OptionalStrType = None,
            expr: OptionalSymPyExprType = None,
            **assumptions: bool) \
            -> Symbol:
        return super().__new__(
                cls,
                name=name
                    if isinstance(name, str) and name
                    else str(uuid4()),
                **assumptions)

    def __init__(
            self,
            name: OptionalStrType = None,
            expr: OptionalSymPyExprType = None,
            **assumptions: bool) \
            -> None:
        self.expr = expr

    @property
    def _short_repr(self) -> str:
        return f"Var {self.name}{f'= {self.expr}' if self.expr else ''}"

    @property
    def free(self):
        return self.expr is None


# alias
Var = Variable


OptionalVariableType = Optional[Variable]