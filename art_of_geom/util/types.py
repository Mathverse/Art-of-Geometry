__all__ = \
    'OptionalStrType', \
    'OptionalSymPyExprType', \
    'print_obj_and_type'


from sympy.core.expr import Expr
from typing import Optional


OptionalStrType = Optional[str]

OptionalSymPyExprType = Optional[Expr]


def print_obj_and_type(obj, /):
    return f'{obj} ({type(obj)}'
