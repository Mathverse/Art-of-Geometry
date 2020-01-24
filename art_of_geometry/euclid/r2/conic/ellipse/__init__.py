__all__ = 'EllipseInR2', 'EllipseR2', 'Ellipse'


from sympy.core.symbol import Symbol
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.geometry.ellipse import Ellipse as SymPyEllipse
from sympy.geometry.exceptions import GeometryError

from ....coord import THETA
from ... import _EuclidR2GeometryEntityABC
from ...coord import X, Y
from ...point import PointInR2


class EllipseInR2(_EuclidR2GeometryEntityABC, SymPyEllipse):
    def __new__(cls, center: PointInR2 = None, hradius: Symbol = None, vradius: Symbol = None, name: str = None):
        assert isinstance(center, PointInR2), \
            GeometryError(
                '*** CENTER {} NOT {} ***'
                .format(center, PointInR2.__name__))

        return super().__new__(
                cls,
                center=center,
                hradius=hradius,
                vradius=vradius)

    def __init__(self, center: PointInR2 = None, hradius: Symbol = None, vradius: Symbol = None, name: str = None):
        # self.center = center

        # self.hradius = hradius

        # self.vradius = vradius

        self._name = name

    @property
    def name(self):
        return self._name \
            if self._name \
          else '{}({}, {})'.format(
                self.center.name,
                self.hradius,
                self.vradius)

    def __repr__(self):
        return 'Ellipse {}'.format(self.name)

    @property
    def equation(self):
        return ((X - self.center.x) / self.hradius) ** 2 \
             + ((Y - self.center.y) / self.vradius) ** 2 \
             - 1

    @property
    def parametric_equations(self):
        return X - self.center.x - self.hradius * cos(THETA), \
               Y - self.center.y - self.vradius * sin(THETA)


# aliases
Ellipse = EllipseR2 = EllipseInR2
