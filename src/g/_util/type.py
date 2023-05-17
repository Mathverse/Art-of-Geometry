"""Data Types."""


from collections.abc import Callable, Sequence
from typing import LiteralString, Optional

from sympy.core.expr import Expr
from sympy.core.numbers import Number


__all__: Sequence[LiteralString] = (
    'Num',
    'OptionalStr',
    'CallableReturningStr', 'OptionalStrOrCallableReturningStr',
    'OptionalSymPyExpr', 'OptionalStrOrSymPyExpr',
    'obj_and_type_str',
)


Num: type = Number | complex | float | int


OptionalStr: type = Optional[str]


CallableReturningStr: type = Callable[[], str]
OptionalStrOrCallableReturningStr: type = Optional[str | CallableReturningStr]


OptionalSymPyExpr: type = Optional[Expr]
OptionalStrOrSymPyExpr: type = Optional[str | Expr]


def obj_and_type_str(obj, /) -> str:
    """Return string representation of object and its type."""
    return f'{obj} ({type(obj)}'
