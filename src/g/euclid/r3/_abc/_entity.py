__all__ = '_EuclideanGeometryEntityInR3ABC',


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ....._util._compat import cached_property
from ...._abc._entity import _GeometryEntityABC


class _EuclideanGeometryEntityInR3ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        raise NotImplementedError
