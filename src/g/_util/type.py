"""Data Types."""


from collections.abc import Sequence
from typing import Callable, Optional, Union

from sympy.core.expr import Expr
from sympy.core.numbers import Number


__all__: Sequence[str] = (
    'NumType',
    'CallableReturningStrType', 'OptionalStrOrCallableReturningStrType',
    'OptionalSymPyExprType', 'OptionalStrOrSymPyExprType',
    'print_obj_and_type',
)


NumType: type = Number | complex | float | int


CallableReturningStrType = Callable[[], str]
OptionalStrOrCallableReturningStrType = Union[str, CallableReturningStrType, None]


OptionalSymPyExprType = Optional[Expr]
OptionalStrOrSymPyExprType = Union[str, Expr, None]


def print_obj_and_type(obj, /):
    return f'{obj} ({type(obj)}'
