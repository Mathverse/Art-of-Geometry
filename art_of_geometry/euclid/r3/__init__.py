__all__ = '_EuclidR3GeometryEntityABC',


from abc import abstractmethod
from functools import cached_property
from sympy.core.expr import Expr
from typing import Tuple

from ... import _GeometryEntityABC


class _EuclidR3GeometryEntityABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        raise NotImplementedError
