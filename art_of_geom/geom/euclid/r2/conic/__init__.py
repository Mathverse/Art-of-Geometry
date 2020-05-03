__all_ = 'ConicInR2', 'ConicR2', 'Conic'


from sympy.core.expr import Expr
from sympy.core.numbers import oo
from sympy.core.singleton import S
from sympy.functions.elementary.trigonometric import atan2, cos, sin
from typing import Tuple

from ....._util._compat import cached_property
from ....var import Variable
from ..._abc._coord import THETA
from .._abc._entity import _EuclideanGeometryEntityInR2ABC
from ..coord import X, Y
from ..line import _LineInR2ABC, LineInR2, LineAtInfinityInR2
from ..point import _PointInR2ABC, PointInR2, PointAtInfinityInR2


@_EuclideanGeometryEntityInR2ABC.assign_name_and_dependencies
class ConicInR2(_EuclideanGeometryEntityInR2ABC):
    def __init__(
            self,
            /, focus: PointInR2, vertex: PointInR2, eccentricity: Variable,
            *, direction_sign: Variable = Variable(S.One)) -> None:
        assert isinstance(focus, PointInR2), \
            TypeError(f'*** FOCUS {focus} NOT OF TYPE {PointInR2.__name__} ***')

        assert isinstance(vertex, PointInR2), \
            TypeError(f'*** VERTEX {vertex} NOT OF TYPE {PointInR2.__name__} ***')

        self.focus = focus

        self.vertex = vertex

        self.focus_to_vertex_direction = vertex - focus
        self.vertex_to_focus_direction = -self.focus_to_vertex_direction

        self.focus_to_vertex_distance = self.focus_to_vertex_direction.euclidean_distance_from_origin

        self.eccentricity = eccentricity
        
        self.direction_sign = direction_sign

    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'{self.focus.name}(vtx: {self.vertex.name}, ecc: {self.eccentricity}, dir: {self.direction_sign})'

    def __repr__(self) -> str:
        return f'Conic {self.name}'

    @cached_property
    def abs_eccentricity(self) -> Variable:
        return Variable(abs(self.eccentricity))

    @cached_property
    def is_circle(self) -> bool:
        return self.eccentricity == S.Zero

    @cached_property
    def is_ellipse(self) -> bool:
        return S.Zero < self.abs_eccentricity < S.One

    @cached_property
    def is_parabola(self) -> bool:
        return self.abs_eccentricity == S.One

    @cached_property
    def is_hyperbola(self) -> bool:
        return S.One < self.abs_eccentricity < oo

    @cached_property
    def is_line(self) -> bool:
        return self.abs_eccentricity == oo

    @cached_property
    def linear_eccentricity(self) -> Expr:
        if self.is_circle:
            return S.Zero

        elif self.is_parabola:
            return oo

        else:
            return self.eccentricity / (1 - self.eccentricity)

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
    def major_axis_line(self) -> LineInR2:
        return LineInR2(self.focus, self.vertex)

    @cached_property
    def minor_axis_line(self) -> _LineInR2ABC:
        if self.is_parabola:
            return LineAtInfinityInR2(self.focus_to_vertex_direction)

        else:
            return self.major_axis_line.perpendicular_line(self.center)

    @cached_property
    def tangent_line_at_vertex(self) -> LineInR2:
        return self.major_axis_line.perpendicular_line(self.vertex)

    @cached_property
    def directrix(self) -> _LineInR2ABC:
        if self.is_circle:
            return LineAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_parabola:
            return self.major_axis_line.perpendicular_line(
                    self.vertex +
                    self.focus_to_vertex_direction)

        elif self.is_line:
            return self.tangent_line_at_vertex.same()

        else:
            return self.major_axis_line.perpendicular_line(
                    self.vertex +
                    self.focus_to_vertex_direction / self.eccentricity)

    @cached_property
    def other_directrix(self) -> _LineInR2ABC:
        if self.is_circle:
            return LineAtInfinityInR2(self.vertex_to_focus_direction)

        elif self.is_parabola:
            return LineAtInfinityInR2(self.focus_to_vertex_direction)

        elif self.is_line:
            return self.tangent_line_at_vertex.same()

        else:
            return self.major_axis_line.perpendicular_line(
                    self.other_vertex +
                    self.vertex_to_focus_direction / self.eccentricity)

    @cached_property
    def directrices(self) -> Tuple[_LineInR2ABC, _LineInR2ABC]:
        return self.directrix, self.other_directrix

    @cached_property
    def major_semi_axis_length(self) -> Expr:
        if self.is_parabola:
            return oo

        else:
            return self.focus_to_vertex_distance / (1 - self.eccentricity)

    # alias
    @cached_property
    def semi_major_axis_length(self) -> Expr:
        return self.major_semi_axis_length

    @cached_property
    def semi_latus_rectum(self):
        if self.is_circle:
            return self.focus_to_vertex_distance

        elif self.is_parabola:
            return 2 * self.focus_to_vertex_distance

        else:
            return (1 + self.eccentricity) * self.focus_to_vertex_distance

    @cached_property
    def _major_axis_angle(self):
        return Variable(
                atan2(y=self.vertex_to_focus_direction.y,
                      x=self.vertex_to_focus_direction.x))

    @cached_property
    def parametric_equations(self) -> Tuple[Expr, Expr]:
        # θ is True Anomaly angle

        signed_theta = self.direction_sign * THETA

        if self.is_circle:
            return X - self.focus.x - self.focus_to_vertex_distance * cos(signed_theta), \
                   Y - self.focus.y - self.focus_to_vertex_distance * sin(signed_theta)

        elif self.is_parabola:
            r = self.semi_latus_rectum / \
                (1 - cos(THETA - self._major_axis_angle))

            return X - self.focus.x - r * cos(signed_theta), \
                   Y - self.focus.y - r * sin(signed_theta)

        elif self.is_line:
            return self.directrix.parametric_equations

        else:
            r = self.semi_latus_rectum / \
                (1 - self.eccentricity * cos(signed_theta - self._major_axis_angle))

            return X - self.focus.x - r * cos(signed_theta), \
                   Y - self.focus.y - r * sin(signed_theta)


# aliases
Conic = ConicR2 = ConicInR2
