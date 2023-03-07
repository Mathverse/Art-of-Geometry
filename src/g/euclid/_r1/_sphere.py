__all__ = \
    'CircleInR1', 'CircleR1', 'Circle', \
    'SphereInR1', 'SphereR1', 'Sphere'


from ...._util._compat import cached_property
from ...var import Variable
from ._abc._entity import _EuclideanGeometryEntityInR1ABC
from .point import PointInR1


class SphereInR1(_EuclideanGeometryEntityInR1ABC):
    def __init__(self, center: PointInR1, radius: Variable) -> None:
        self.center = center
        self.radius = radius

    @cached_property
    def point_0(self) -> PointInR1:
        return PointInR1(self.center - self.radius)

    @cached_property
    def point_1(self) -> PointInR1:
        return PointInR1(self.center + self.radius)

    @cached_property
    def points(self):
        return self.point_0, self.point_1


# aliases
Circle = CircleR1 = CircleInR1 = Sphere = SphereR1 = SphereInR1
