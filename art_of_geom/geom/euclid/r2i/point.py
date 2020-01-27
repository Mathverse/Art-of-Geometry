__all__ = 'PointInR2_DoubleConeInR2I',


from sympy.geometry.exceptions import GeometryError

from ..r2.point import PointInR2
from .abc import _SurfaceInR2IABC
from .coord import X, Y, Z


class PointInR2_DoubleConeInR2I(_SurfaceInR2IABC):
    def __init__(self, point_in_r2: PointInR2):
        assert isinstance(point_in_r2, PointInR2), \
            GeometryError(
                '*** {} NOT {} ***'
                .format(point_in_r2, PointInR2.__name__))

        self.point_in_r2 = point_in_r2

    @property
    def equation(self):
        return (X - self.point_in_r2.x) ** 2 \
             + (Y - self.point_in_r2.y) ** 2 \
             - Z ** 2
