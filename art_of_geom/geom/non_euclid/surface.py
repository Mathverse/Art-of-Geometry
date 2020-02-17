__all__ = '_NonEuclidSurfaceABC',


from art_of_geom.geom._abc._entity import _GeometryEntityABC


class _NonEuclidSpaceABC:
    pass


class _NonEuclidSurfaceABC(_NonEuclidSpaceABC, _GeometryEntityABC):
    pass
