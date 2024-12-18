from sympy.geometry.polygon import Polygon

from g.geom._core._entity import _GeometryEntityABC


class Quadrilateral(Polygon, _GeometryEntityABC):
    pass


# alias
Quadrangle = Quadrilateral
