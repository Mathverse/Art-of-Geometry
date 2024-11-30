__all__ = 'SphereInRD', 'SphereRD', 'Sphere'


from ..core._entity import _EuclideanGeometryEntityABC


class SphereInRD(_EuclideanGeometryEntityABC):
    pass


# aliases
Sphere = SphereRD = SphereInRD
