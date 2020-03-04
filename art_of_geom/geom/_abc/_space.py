__all__ = '_SpaceABC',


from ._entity import _GeometryEntityABC
from ._point import _ConcretePointABC


class _SpaceABC(_GeometryEntityABC):
    pass


class _HalfSpaceABC(_GeometryEntityABC):
    def __init__(self, boundary: _SpaceABC, normal_vector: _ConcretePointABC) -> None:
        self.boundary = boundary
        self.normal_vector = normal_vector
