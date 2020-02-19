__all__ = 'PointInR0', 'PointR0', 'Point', 'Pt'


from ..._abc._point import _EuclideanConcretePointABC


@_EuclideanConcretePointABC.assign_name_and_dependencies
class _PointInR0(_EuclideanConcretePointABC):
    pass


# singleton aliases
Pt = Point = PointR0 = PointInR0 = _PointInR0(name='SINGULARITY')
