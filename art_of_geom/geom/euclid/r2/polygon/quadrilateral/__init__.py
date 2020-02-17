from sympy.geometry.polygon import Polygon

from art_of_geom.geom._abc._entity import _GeometryEntityABC


class Quadrilateral(Polygon, _GeometryEntityABC):
    pass


# alias
Quadrangle = Quadrilateral
