__all__ = \
    '_LinearEntityABC', '_ConcreteLinearEntityABC', '_LinearEntityAtInfinityABC', \
    '_LineABC', '_ConcreteLineABC', '_LineAtInfinityABC'


from abc import abstractmethod

from . import _GeometryEntityABC
from .point import _PointABC


class _LinearEntityABC(_GeometryEntityABC):
    @abstractmethod
    def parallel_line(self, through_point: _PointABC, /, *, name=None):
        raise NotImplementedError

    @abstractmethod
    def perpendicular_projection(self, point: _PointABC, /, *, name=None) -> _PointABC:
        raise NotImplementedError

    @abstractmethod
    def perpendicular_line(self, through_point: _PointABC, /, *, name=None):
        raise NotImplementedError


class _ConcreteLinearEntityABC(_LinearEntityABC):
    pass


class _LinearEntityAtInfinityABC(_LinearEntityABC):
    pass


class _LineABC(_LinearEntityABC):
    @abstractmethod
    def perspective_projection(self, /, perspector: _PointABC, point: _PointABC, *, name=None) -> _PointABC:
        raise NotImplementedError


class _ConcreteLineABC(_LineABC, _ConcreteLinearEntityABC):
    pass


class _LineAtInfinityABC(_LineABC, _LinearEntityAtInfinityABC):
    pass
