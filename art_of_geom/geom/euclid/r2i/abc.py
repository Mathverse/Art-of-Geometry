__all__ = '_EuclidGeometryEntityInR2IABC', '_SurfaceInR2IABC'


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ...._util._compat import cached_property
from art_of_geom.geom._abc._entity import _GeometryEntityABC


class _EuclidGeometryEntityInR2IABC(_GeometryEntityABC):
    def __repr__(self) -> str:
        return f'{self.session._str_prefix}Euclid.R2I {self._short_repr}'

    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        raise NotImplementedError


class _SurfaceInR2IABC(_EuclidGeometryEntityInR2IABC):
    pass
