__all__ = 'PointInR0', 'PointR0', 'Point', 'Pt'


from ...._util._tmp import TMP_NAME_FACTORY
from .._abc._point import _EuclideanConcretePointABC


@_EuclideanConcretePointABC.assign_name_and_dependencies
class _PointInR0(_EuclideanConcretePointABC):
    @property
    def name(self) -> str:
        return getattr(self, self._NAME_ATTR_KEY)

    @name.setter
    def name(self, name: str, /) -> None:
        self._validate_name(name)

        if name != getattr(self, self._NAME_ATTR_KEY):
            setattr(self, self._NAME_ATTR_KEY, name)

    @name.deleter
    def name(self):
        setattr(self, self._NAME_ATTR_KEY, TMP_NAME_FACTORY())


# singleton aliases
Pt = Point = PointR0 = PointInR0 = _PointInR0(name='SINGULARITY')
