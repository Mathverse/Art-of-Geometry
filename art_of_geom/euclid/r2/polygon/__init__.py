from sympy.geometry.polygon import Polygon as SymPyPolygon

from .. import _EuclidGeometryEntityInR2ABC
from ..point import PointInR2


class Polygon(_EuclidGeometryEntityInR2ABC, SymPyPolygon):
    def __new__(cls, *points: PointInR2, n: int = None, name=None):
        assert all(isinstance(point, PointInR2)
                   for point in points)

        polygon = super().__new__(cls, *points)
