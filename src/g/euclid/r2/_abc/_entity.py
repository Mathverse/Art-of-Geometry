__all__ = '_EuclideanGeometryEntityInR2ABC',


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ....._util._compat import cached_property
from ...._core._entity import _GeometryEntityABC


class _EuclideanGeometryEntityInR2ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        raise NotImplementedError
