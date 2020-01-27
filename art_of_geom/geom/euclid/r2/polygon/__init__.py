__all__ = 'PolygonInR2', 'PolygonR2', 'Polygon'


from sympy.geometry.polygon import Polygon as Polygon2D

from ..abc import _EuclidGeometryEntityInR2ABC
from ..point import PointInR2


class PolygonInR2(_EuclidGeometryEntityInR2ABC, Polygon2D):
    def __new__(cls, *points: PointInR2, n: int = None, name=None):
        assert all(isinstance(point, PointInR2)
                   for point in points)

        polygon = super().__new__(cls, *points)


# aliases
Polygon = PolygonR2 = PolygonInR2