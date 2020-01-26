__all__ = '_LineABC'


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


class _LineABC(_LinearEntityABC):
    @abstractmethod
    def perspective_projection(self, /, perspector: _PointABC, point: _PointABC, *, name=None) -> _PointABC:
        raise NotImplementedError
