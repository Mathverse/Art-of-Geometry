__all__ = '_SpaceABC', '_HalfSpaceABC'


from ._entity import _GeometryEntityABC
from ._point import _ConcretePointABC


class _SpaceABC(_GeometryEntityABC):
    pass


class _HalfSpaceABC(_GeometryEntityABC):
    def __init__(self, boundary: _SpaceABC, point: _ConcretePointABC) -> None:
        self.boundary = boundary
        self.point = point
