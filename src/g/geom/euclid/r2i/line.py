__all__ = 'LineInR2_VerticalPlaneInR2I',


from sympy.geometry.exceptions import GeometryError

from ..r2.line import LineInR2
from .abc import _SurfaceInR2IABC


class LineInR2_VerticalPlaneInR2I(_SurfaceInR2IABC):
    def __init__(self, line_in_r2: LineInR2):
        assert isinstance(line_in_r2, LineInR2), \
            GeometryError(
            '*** {} NOT {} ***'
                .format(line_in_r2, LineInR2.__name__))

        self.line_in_r2 = line_in_r2

    @property
    def equation(self):
        return self.line_in_r2.equation

    @property
    def parametric_equations(self):
        return self.line_in_r2.parametric_equations
