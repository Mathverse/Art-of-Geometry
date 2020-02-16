__all__ = \
    'OptionalStrType', \
    'OptionalSymPyExprType'


from sympy.core.expr import Expr
from typing import Optional


OptionalStrType = Optional[str]

OptionalSymPyExprType = Optional[Expr]
