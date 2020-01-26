__all__ = '_EuclidR2GeometryEntityABC',


from abc import abstractmethod
from functools import cached_property
from sympy.core.expr import Expr
from typing import Tuple

from ... import _GeometryEntityABC


class _EuclidR2GeometryEntityABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        raise NotImplementedError
