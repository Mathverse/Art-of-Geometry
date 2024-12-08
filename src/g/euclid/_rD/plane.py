__all__ = 'PlaneInRD', 'PlaneRD', 'Plane'


from .._core._entity import AnEuclidGeomEntity


class PlaneInRD(AnEuclidGeomEntity):
    pass


# aliases
Plane = PlaneRD = PlaneInRD
