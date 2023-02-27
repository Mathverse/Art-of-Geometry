__all__ = 'HyperbolaInR2', 'HyperbolaR2', 'Hyperbola'


from sympy.assumptions.ask import Q
from sympy.assumptions.assume import global_assumptions
from sympy.core.singleton import S

from ....var import Variable
from ..point import PointInR2
from . import ConicInR2


@ConicInR2.assign_name_and_dependencies
class HyperbolaInR2(ConicInR2):
    def __init__(
            self,
            /, focus: PointInR2, vertex: PointInR2, eccentricity: Variable,
            *, direction_sign: Variable = Variable(S.One)) -> None:
        global_assumptions.add(
            Q.positive(eccentricity - S.One),
            Q.finite(eccentricity))

        super().__init__(
            focus=focus,
            vertex=vertex,
            eccentricity=eccentricity)

    def __repr__(self) -> str:
        return f'Hyperbola {self.name}'


# aliases
Hyperbola = HyperbolaR2 = HyperbolaInR2
