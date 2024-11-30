__all__ = 'PlaneInRD', 'PlaneRD', 'Plane'


from ..core._entity import _EuclideanGeometryEntityABC


class PlaneInRD(_EuclideanGeometryEntityABC):
    pass


# aliases
Plane = PlaneRD = PlaneInRD
