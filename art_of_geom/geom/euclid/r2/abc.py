__all__ = '_EuclidGeometryEntityInR2ABC',


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ....util.compat import cached_property
from ...abc import _GeometryEntityABC


class _EuclidGeometryEntityInR2ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        raise NotImplementedError
