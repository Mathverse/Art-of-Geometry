__all_ = 'ConicInR2', 'ConicR2', 'Conic'


from functools import cached_property
from sympy.core.expr import Expr
from sympy.core.numbers import oo
from sympy.core.singleton import S
from sympy.functions.elementary.trigonometric import atan2, cos, sin
from sympy.geometry.exceptions import GeometryError
from typing import Tuple

from ...coord import THETA
from .. import _EuclidR2GeometryEntityABC
from ..coord import X, Y
from ..line import _LineInR2ABC, LineInR2, LineAtInfinityInR2
from ..point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


class ConicInR2(_EuclidR2GeometryEntityABC):
    def __init__(self, /, focus: PointInR2, vertex: PointInR2, eccentricity: Expr, *, name: str = None) -> None:
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

        self.focus_to_vertex_direction = vertex - focus
        self.vertex_to_focus_direction = -self.focus_to_vertex_direction

        self.focus_to_vertex_distance = self.focus_to_vertex_direction.distance_from_origin

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

    @cached_property
    def is_circle(self):
        return self.eccentricity == S.Zero

    @cached_property
    def is_parabola(self):
        return self.eccentricity == S.One

    @cached_property
    def is_line(self):
        return self.eccentricity == oo

    @cached_property
    def _major_axis_angle(self):
        return atan2(y=self.vertex_to_focus_direction.y,
                     x=self.vertex_to_focus_direction.x)

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        if self.is_circle:
            return X - self.focus.x - self.focus_to_vertex_distance * cos(THETA), \
                   Y - self.focus.y - self.focus_to_vertex_distance * sin(THETA)

        elif self.is_parabola:
            pass

        elif self.is_line:
            pass

        else:
            phi = self._major_axis_angle

            r = (1 - self.eccentricity) * self.focus_to_vertex_distance / \
                (1 - self.eccentricity * cos(THETA - phi))

            return X - self.focus.x - r * cos(THETA + phi), \
                   Y - self.focus.y - r * sin(THETA + phi)

    @cached_property
    def center(self) -> _PointInR2ABC:
        if self.is_circle:
            return self.focus.same()

        elif self.is_parabola:
            return PointAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_line:
            return self.vertex.same()

        else:
            return self.vertex \
                 + self.vertex_to_focus_direction / (1 - self.eccentricity)

    @cached_property
    def other_focus(self) -> _PointInR2ABC:
        if self.is_circle:
            return self.focus.same()

        elif self.is_parabola:
            return PointAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_line:
            return self.vertex + self.focus_to_vertex_direction

        else:
            return self.vertex \
                 + (1 + self.eccentricity) / (1 - self.eccentricity) * self.vertex_to_focus_direction

    @cached_property
    def foci(self) -> Tuple[PointInR2, _PointInR2ABC]:
        return self.focus, self.other_focus

    @cached_property
    def other_vertex(self) -> _PointInR2ABC:
        if self.is_circle:
            return self.focus + self.vertex_to_focus_direction

        elif self.is_parabola:
            return PointAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_line:
            return self.vertex.same()

        else:
            return self.vertex \
                 + 2 * self.vertex_to_focus_direction / (1 - self.eccentricity)

    @cached_property
    def vertices(self) -> Tuple[PointInR2, _PointInR2ABC]:
        return self.vertex, self.other_vertex

    @cached_property
    def major_axis(self):
        return LineInR2(self.focus, self.vertex)

    @cached_property
    def minor_axis(self):
        return self.major_axis.perpendicular_line(self.center)

    @cached_property
    def directrix(self) -> _LineInR2ABC:
        if self.is_circle:
            return LineAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_parabola:
            return self.major_axis.perpendicular_line(
                    self.vertex +
                    self.focus_to_vertex_direction)

        elif self.is_line:
            return self.major_axis.perpendicular_line(self.vertex)

        else:
            return self.major_axis.perpendicular_line(
                    self.vertex +
                    self.focus_to_vertex_direction / self.eccentricity)

    @cached_property
    def other_directrix(self) -> _LineInR2ABC:
        if self.is_circle:
            return LineAtInfinityInR2(self.vertex_to_focus_direction)

        elif self.is_parabola:
            return LineAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_line:
            return self.major_axis.perpendicular_line(self.vertex)

        else:
            return self.major_axis.perpendicular_line(
                    self.other_vertex +
                    self.vertex_to_focus_direction / self.eccentricity)

    @cached_property
    def directrices(self):
        return self.directrix, self.other_directrix


# aliases
Conic = ConicR2 = ConicInR2
