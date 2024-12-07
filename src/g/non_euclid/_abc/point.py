__all__ = '_NonEuclidPointABC', '_NonEuclidConcretePointABC', '_NonEuclidPointAtInfinityABC'


from g.geom._core._point import APoint, AConcretePoint, APointAtInf


class _NonEuclidPointABC(APoint):
    pass


class _NonEuclidConcretePointABC(_NonEuclidPointABC, AConcretePoint):
    pass


class _NonEuclidPointAtInfinityABC(_NonEuclidPointABC, APointAtInf):
    pass
