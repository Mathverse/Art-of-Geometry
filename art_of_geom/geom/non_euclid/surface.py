__all__ = '_NonEuclideanSurfaceABC',


from art_of_geom.geom._abc._entity import _GeometryEntityABC


class _NonEuclideanSpaceABC:
    pass


class _NonEuclideanSurfaceABC(_NonEuclideanSpaceABC, _GeometryEntityABC):
    pass
