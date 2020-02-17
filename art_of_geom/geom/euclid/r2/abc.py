__all__ = '_EuclidGeometryEntityInR2ABC',


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ...._util._compat import cached_property
from art_of_geom.geom._abc._entity import _GeometryEntityABC


class _EuclidGeometryEntityInR2ABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        raise NotImplementedError
