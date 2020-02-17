__all__ = '_EuclidGeometryEntityInR3ABC',


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ....util.compat import cached_property
from ...abc import _GeometryEntityABC


class _EuclidGeometryEntityInR3ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        raise NotImplementedError
