__all__ = \
    'PointInRD', 'PointRD', 'Point', 'Pt', \
    'PointAtInfinityInRD', 'PointAtInfinityRD', 'PointAtInfinity', 'PtAtInf'



from .._abc._point import _EuclideanConcretePointABC, _EuclideanPointAtInfinityABC





class PointInRD(_EuclideanConcretePointABC):
    pass


# aliases
Pt = Point = PointRD = PointInRD


class PointAtInfinityInRD(_EuclideanPointAtInfinityABC):
    pass


# aliases
PtAtInf = PointAtInfinity = PointAtInfinityRD = PointAtInfinityInRD
