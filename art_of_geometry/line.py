__all__ = '_LineABC'


from abc import abstractmethod

from . import _GeometryEntityABC
from .point import _PointABC


class _LineABC(_GeometryEntityABC):
    @abstractmethod
    def parallel_line(self, through_point: _PointABC, /, *, name=None):
        raise NotImplementedError

    @abstractmethod
    def perpendicular_line(self, through_point: _PointABC, /, *, name=None):
        raise NotImplementedError
