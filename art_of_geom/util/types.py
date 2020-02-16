__all__ = \
    'OptionalStrType', \
    'OptionalSymPyExprType', \
    'OptionalStrOrSymPyExprType', \
    'print_obj_and_type'


from sympy.core.expr import Expr
from typing import Optional, Union


OptionalStrType = Optional[str]

OptionalSymPyExprType = Optional[Expr]

OptionalStrOrSymPyExprType = Union[Expr, str, None]


def print_obj_and_type(obj, /):
    return f'{obj} ({type(obj)}'
