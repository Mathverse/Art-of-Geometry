__all__ = '_NonEuclidPointABC', '_NonEuclidConcretePointABC', '_NonEuclidPointAtInfinityABC'


from art_of_geom.geom._abc._point import _PointABC, _ConcretePointABC, _PointAtInfinityABC


class _NonEuclidPointABC(_PointABC):
    pass


class _NonEuclidConcretePointABC(_NonEuclidPointABC, _ConcretePointABC):
    pass


class _NonEuclidPointAtInfinityABC(_NonEuclidPointABC, _PointAtInfinityABC):
    pass
