"""Data Types."""


from collections.abc import Callable, Sequence
from typing import LiteralString

from sympy.core.expr import Expr
from sympy.core.numbers import Number, RealNumber


__all__: Sequence[LiteralString] = (
    'Num', 'RealNum',
    'OptionalStr',
    'CallableReturningStr', 'OptionalStrOrCallableReturningStr',
    'OptionalSymPyExpr', 'OptionalStrOrSymPyExpr',
    'obj_and_type_str',
)


Num: type = Number | complex | float | int
RealNum: type = RealNumber | float


OptionalStr: type = str | None


CallableReturningStr: type = Callable[[], str]
OptionalStrOrCallableReturningStr: type = str | CallableReturningStr | None


OptionalSymPyExpr: type = Expr | None
OptionalStrOrSymPyExpr: type = str | Expr | None


def obj_and_type_str(obj, /) -> str:
    """Return string representation of object and its type."""
    return f'{obj} ({type(obj)}'
