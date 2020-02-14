from sympy.geometry.polygon import Polygon

from .....abc import _GeometryEntityABC


class Quadrilateral(Polygon, _GeometryEntityABC):
    pass


# alias
Quadrangle = Quadrilateral
