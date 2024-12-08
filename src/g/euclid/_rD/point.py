__all__ = \
    'PointInRD', 'PointRD', 'Point', 'Pt', \
    'PointAtInfinityInRD', 'PointAtInfinityRD', 'PointAtInfinity', 'PtAtInf'



from .._core._point import AEuclidConcretePoint, AnEuclidPointAtInf





class PointInRD(AEuclidConcretePoint):
    pass


# aliases
Pt = Point = PointRD = PointInRD


class PointAtInfinityInRD(AnEuclidPointAtInf):
    pass


# aliases
PtAtInf = PointAtInfinity = PointAtInfinityRD = PointAtInfinityInRD
