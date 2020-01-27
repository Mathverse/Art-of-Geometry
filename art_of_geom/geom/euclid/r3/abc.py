__all__ = '_EuclidGeometryEntityInR3ABC',


from abc import abstractmethod
from functools import cached_property
from sympy.core.expr import Expr
from typing import Tuple

from ...abc import _GeometryEntityABC


class _EuclidGeometryEntityInR3ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        raise NotImplementedError
