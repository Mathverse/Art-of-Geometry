__all__ = 'EllipseInR2', 'EllipseR2', 'Ellipse'


from sympy.core.symbol import Symbol
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.geometry.ellipse import Ellipse as SymPyEllipse
from sympy.geometry.exceptions import GeometryError

from ....coord import THETA
from ... import _EuclidR2GeometryEntityABC
from ...coord import X, Y
from ...point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


class EllipseInR2(_EuclidR2GeometryEntityABC, SymPyEllipse):
    def __new__(cls, focus: PointInR2, vertex: PointInR2, eccentricity: Symbol = None, name: str = None):
        assert isinstance(focus, PointInR2), \
            GeometryError(
                '*** FOCUS {} NOT {} ***'
                .format(focus, PointInR2.__name__))

        assert isinstance(vertex, PointInR2), \
            GeometryError(
                '*** VERTEX {} NOT {} ***'
                .format(vertex, PointInR2.__name__))

        direction = focus - vertex

        hradius = focus.distance(other=vertex) / (1 - eccentricity)

        ellipse = super().__new__(
                    cls,
                    center=vertex + hradius * direction.unit,
                    hradius=hradius,
                    eccentricity=eccentricity)

        ellipse.direction = direction

        return ellipse

    def __init__(self, focus: PointInR2, vertex: PointInR2, eccentricity: Symbol = None, name: str = None):
        self.focus = focus

        self.vertex = vertex

        # self.eccentricity = eccentricity

        self._name = name

    @property
    def name(self):
        return self._name \
            if self._name \
          else '{}(vtx: {}, ecc: {})'.format(
                self.focus.name,
                self.vertex.name,
                self.eccentricity)

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
