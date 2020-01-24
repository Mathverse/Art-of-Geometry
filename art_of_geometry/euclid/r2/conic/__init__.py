__all_ = 'ConicInR2', 'ConicR2', 'Conic'


from sympy.core.symbol import Symbol

from .. import _EuclidR2GeometryEntityABC
from ..point import PointInR2


class ConicInR2(_EuclidR2GeometryEntityABC):
    def __init__(self, focus: PointInR2, vertex: PointInR2, eccentricity: Symbol, name: str = None):
        self.focus = focus

        self.vertex = vertex

        self.eccentricity = eccentricity

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
        return 'Conic {}'.format(self.name)


# aliases
Conic = ConicR2 = ConicInR2
