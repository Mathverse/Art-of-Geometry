__all__ = 'ParabolaInR2', 'ParabolaR2', 'Parabola'


from sympy.core.singleton import S
from sympy.geometry.parabola import Parabola as Parabola2D
from typing import Optional

from ..point import PointInR2
from . import ConicInR2


class ParabolaInR2(ConicInR2):
    def __init__(
            cls,
            /, focus: PointInR2, vertex: PointInR2,
            *, name: Optional[str] = None) \
            -> None:
        super().__init__(
            focus=focus,
            vertex=vertex,
            eccentricity=S.One,
            name=name)

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.focus.name}(vtx: {self.vertex.name})'

    def __repr__(self) -> str:
        return f'Parabola {self.name}'


# aliases
Parabola = ParabolaR2 = ParabolaInR2
