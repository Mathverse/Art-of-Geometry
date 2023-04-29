"""Data Types."""


from collections.abc import Callable, Sequence
from typing import Optional

from sympy.core.expr import Expr
from sympy.core.numbers import Number


__all__: Sequence[str] = (
    'Num',
    'CallableReturningStr', 'OptionalStrOrCallableReturningStr',
    'OptionalSymPyExpr', 'OptionalStrOrSymPyExpr',
    'print_obj_and_type',
)


Num: type = Number | complex | float | int


CallableReturningStr: type = Callable[[], str]
OptionalStrOrCallableReturningStr: type = Optional[str | CallableReturningStr]


OptionalSymPyExpr: type = Optional[Expr]
OptionalStrOrSymPyExpr: type = Optional[str | Expr]


def print_obj_and_type(obj, /):
    """Print object and its type."""
    return f'{obj} ({type(obj)}'
