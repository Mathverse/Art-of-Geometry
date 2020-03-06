__all__ = 'ParabolaInR2', 'ParabolaR2', 'Parabola'


from sympy.core.singleton import S

from ..point import PointInR2
from . import ConicInR2


@ConicInR2.assign_name_and_dependencies
class ParabolaInR2(ConicInR2):
    def __init__(self, /, focus: PointInR2, vertex: PointInR2) -> None:
        super().__init__(
            focus=focus,
            vertex=vertex,
            eccentricity=S.One)

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.focus.name}(vtx: {self.vertex.name})'

    def __repr__(self) -> str:
        return f'Parabola {self.name}'


# aliases
Parabola = ParabolaR2 = ParabolaInR2
