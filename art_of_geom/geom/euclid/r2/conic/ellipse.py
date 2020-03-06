__all__ = 'EllipseInR2', 'EllipseR2', 'Ellipse'


from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.singleton import S

from ....var import Variable
from ..point import PointInR2
from . import ConicInR2


@ConicInR2.assign_name_and_dependencies
class EllipseInR2(ConicInR2):
    def __init__(self, /, focus: PointInR2, vertex: PointInR2, eccentricity: Variable) -> None:
        global_assumptions.add(Q.negative(eccentricity - S.One))

        super().__init__(
            focus=focus,
            vertex=vertex,
            eccentricity=eccentricity)

    def __repr__(self) -> str:
        return 'Ellipse {}'.format(self.name)


# aliases
Ellipse = EllipseR2 = EllipseInR2
