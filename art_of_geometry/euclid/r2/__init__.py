__all__ = '_EuclidGeometryEntityInR2ABC',


from abc import abstractmethod
from functools import cached_property
from sympy.core.expr import Expr
from typing import Tuple

from ... import _GeometryEntityABC


class _EuclidGeometryEntityInR2ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        raise NotImplementedError
