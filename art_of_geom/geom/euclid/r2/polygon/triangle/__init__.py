__all__ = 'TriangleInR2', 'TriangleR2', 'Triangle'


from sympy.geometry.polygon import Triangle as Triangle2D
from sympy.geometry.exceptions import GeometryError

from art_of_geom.geom._abc._entity import _GeometryEntityABC
from ...point import PointInR2


class TriangleInR2(Triangle2D, _GeometryEntityABC):
    def __new__(cls, *vertices: PointInR2, name: str = None):
        assert len(vertices) == 3, \
            GeometryError
        
        assert all(isinstance(vertex, PointInR2)
                   for vertex in vertices)

        return super().__new__(cls, *vertices)
    
    def __init__(self, *vertices: PointInR2, name: str = None):
        self.vertex_0, self.vertex_1, self.vertex_2 = vertices

        self._name = name

    @property
    def name(self):
        return self._name \
            if self._name \
          else '{} *-> {} *-> {}'.format(
                self.vertex_0.name,
                self.vertex_1.name,
                self.vertex_2.name)

    def __repr__(self):
        return 'Triangle {}'.format(self.name)


# aliases
Triangle = TriangleR2 = TriangleInR2
