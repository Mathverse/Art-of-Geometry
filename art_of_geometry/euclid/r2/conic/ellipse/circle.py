__all__ = \
    'CircleInR2',


from sympy.core.symbol import Symbol
from sympy.geometry.ellipse import Circle as SymPyCircle

from ..... import _GeometryEntityABC
from ...coord import X, Y
from ...point import PointInR2


class CircleInR2(SymPyCircle, _GeometryEntityABC):
    def __new__(cls, center: PointInR2 = None, radius: Symbol = None, name: str = None):
        return super().__new__(
                cls,
                center=center,
                radius=radius)

    def __init__(self, center: PointInR2 = None, radius: Symbol = None, name: str = None):
        self.center = center

        self.radius = radius

        self._name = name

    @property
    def equation(self):
        return (X - self.circle_in_r2.center.x) ** 2 \
             + (Y - self.circle_in_r2.center.y) ** 2 \
             - self.circle_in_r2.radius ** 2
