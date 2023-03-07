from sympy.core.mod import Mod
from sympy.core.numbers import pi
from sympy.core.singleton import S

from ._abc._entity import _EuclideanGeometryEntityInR2ABC
from .line import LineInR2, RayInR2


class _AngleABC(_EuclideanGeometryEntityInR2ABC):
    pass


class AngleBetweenLines(_AngleABC):
    def __init__(self, line_0: LineInR2, line_1: LineInR2):
        self.line_0 = line_0
        self.line_1 = line_1

        self.signed_measure = None

    def __eq__(self, angle_between_lines):
        assert isinstance(angle_between_lines, AngleBetweenLines)

        return Mod(self.signed_measure - angle_between_lines.signed_measure, pi) is S.Zero


class AngleBetweenRays(_AngleABC):
    def __init__(self, ray_0: RayInR2, ray_1: RayInR2):
        self.ray_0 = ray_0
        self.ray_1 = ray_1

        self.signed_measure = None

    def __eq__(self, angle_between_rays):
        assert isinstance(angle_between_rays, AngleBetweenRays)

        return Mod(self.signed_measure - angle_between_rays.signed_measure, 2 * pi) is S.Zero


# class AngleBetweenSameOriginRays(AngleBetweenRays):
