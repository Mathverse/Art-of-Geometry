__all_ = 'ConicInR2', 'ConicR2', 'Conic'


from sympy.core.expr import Expr
from sympy.core.singleton import S
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.geometry.exceptions import GeometryError
from typing import Tuple

from ...coord import THETA
from .. import _EuclidR2GeometryEntityABC
from ..coord import X, Y
from ..line import _LineInR2ABC, LineInR2, LineAtInfinityInR2
from ..point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


class ConicInR2(_EuclidR2GeometryEntityABC):
    def __init__(self, focus: PointInR2, vertex: PointInR2, eccentricity: Expr, name: str = None) -> None:
        assert isinstance(focus, PointInR2), \
            GeometryError(
                '*** FOCUS {} NOT OF TYPE {} ***'
                .format(focus, PointInR2.__name__))

        assert isinstance(vertex, PointInR2), \
            GeometryError(
                '*** VERTEX {} NOT OF TYPE {} ***'
                .format(vertex, PointInR2.__name__))

        self.focus = focus

        self.vertex = vertex

        self.direction = (focus - vertex).unit

        self.eccentricity = eccentricity

        self._name = name

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else '{}(vtx: {}, ecc: {})'.format(
                self.focus.name,
                self.vertex.name,
                self.eccentricity)

    def __repr__(self) -> str:
        return 'Conic {}'.format(self.name)

    @property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        pass

    @property
    def other_focus(self) -> _PointInR2ABC:
        if self.eccentricity == S.One:   # parabola
            return PointAtInfinityInR2(direction=self.direction)

    @property
    def foci(self) -> Tuple[PointInR2, _PointInR2ABC]:
        return self.focus, self.other_focus

    @property
    def other_vertex(self) -> _PointInR2ABC:
        if self.eccentricity == S.One:   # parabola
            return PointAtInfinityInR2(direction=self.direction)

        else:
            pass

    @property
    def vertices(self) -> Tuple[PointInR2, _PointInR2ABC]:
        return self.vertex, self.other_vertex

    @property
    def directrix(self) -> _LineInR2ABC:
        if self.eccentricity == S.One:   # parabola
            return LineAtInfinityInR2(normal_direction=self.direction)

        else:
            pass

    @property
    def other_directrix(self) -> _LineInR2ABC:
        if self.eccentricity == S.One:   # parabola
            return LineAtInfinityInR2(normal_direction=self.direction)

        else:
            pass


# aliases
Conic = ConicR2 = ConicInR2
