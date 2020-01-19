from sympy.geometry.polygon import Triangle as SymPyTriangle

from ..... import _GeometryEntityABC


class Triangle(SymPyTriangle, _GeometryEntityABC):
    def __init__(self):
        pass
