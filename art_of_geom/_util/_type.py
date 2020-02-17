__all__ = \
    'NUMERIC_TYPES', \
    'OptionalStrType', \
    'OptionalSymPyExprType', \
    'OptionalStrOrSymPyExprType', \
    'print_obj_and_type'


from sympy.core.expr import Expr
from sympy.core.numbers import Number
from typing import Optional, Union


NUMERIC_TYPES = Number, complex, float, int

OptionalStrType = Optional[str]

OptionalSymPyExprType = Optional[Expr]

OptionalStrOrSymPyExprType = Union[Expr, str, None]


def print_obj_and_type(obj, /):
    return f'{obj} ({type(obj)}'
