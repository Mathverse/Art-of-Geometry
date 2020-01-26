__all__ = '_PointABC'


from functools import cached_property
from sympy.core.expr import Expr

from . import _GeometryEntityABC


class _PointABC(_GeometryEntityABC):
    @cached_property
    def distance_from_origin(self) -> Expr:
        raise NotImplementedError
