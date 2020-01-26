__all__ = '_EuclidGeometryEntityInR2IABC', '_SurfaceInR2IABC'


from abc import abstractmethod
from functools import cached_property
from sympy.core.expr import Expr
from typing import Tuple


from ... import _GeometryEntityABC


class _EuclidGeometryEntityInR2IABC(_GeometryEntityABC):
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr, Expr]:
        raise NotImplementedError


class _SurfaceInR2IABC(_EuclidGeometryEntityInR2IABC):
    pass
