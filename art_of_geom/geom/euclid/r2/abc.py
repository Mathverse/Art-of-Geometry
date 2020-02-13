__all__ = '_EuclidGeometryEntityInR2ABC',


from abc import abstractmethod
from sympy.core.expr import Expr
from typing import Tuple

from ....util.compat import cached_property
from ...abc import _GeometryEntityABC


class _EuclidGeometryEntityInR2ABC(_GeometryEntityABC):
    def __str__(self) -> str:
        return f'{self.session._str_prefix}Euclid.R2 {repr(self)}'

    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        raise NotImplementedError
