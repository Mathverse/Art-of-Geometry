from __future__ import annotations


__all__ = \
    '_LinearEntityABC', '_ConcreteLinearEntityABC', '_LinearEntityAtInfinityABC', \
    '_LineABC', '_ConcreteLineABC', '_ConcreteDirectedLineABC', '_LineAtInfinityABC', '_DirectedLineAtInfinityABC'


from abc import abstractmethod

from ._entity import _GeometryEntityABC
from ._point import _PointABC


class _LinearEntityABC(_GeometryEntityABC):
    @abstractmethod
    def parallel_line(self, through_point: _PointABC, /) -> _LineABC:
        raise NotImplementedError

    @abstractmethod
    def perpendicular_projection_of_point(self, point: _PointABC, /) -> _PointABC:
        raise NotImplementedError

    # alias
    def perpendicular_projection(self, point: _PointABC, /) -> _PointABC:
        return self.perpendicular_projection_of_point(point)

    @abstractmethod
    def perpendicular_line(self, through_point: _PointABC, /) -> _LineABC:
        raise NotImplementedError


class _ConcreteLinearEntityABC(_LinearEntityABC):
    pass


class _LinearEntityAtInfinityABC(_LinearEntityABC):
    pass


class _LineABC(_LinearEntityABC):
    @abstractmethod
    def perspective_projection_of_point(self, /, perspector: _PointABC, point: _PointABC) -> _PointABC:
        raise NotImplementedError

    # alias
    def perspective_projection(self, /, perspector: _PointABC, point: _PointABC) -> _PointABC:
        return self.perspective_projection_of_point(perspector=perspector, point=point)


class _ConcreteLineABC(_LineABC, _ConcreteLinearEntityABC):
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'-{self.point_0.name}--{self.point_1.name}-'

    @property
    def _short_repr(self) -> str:
        return f'Ln {self.name}'


class _ConcreteDirectedLineABC(_ConcreteLineABC):
    @property
    def name(self) -> str:
        return self._name \
            if self._name \
          else f'-{self.point_0.name}->{self.point_1.name}-'

    @property
    def _short_repr(self) -> str:
        return f'DirLn {self.name}'


class _LineAtInfinityABC(_LineABC, _LinearEntityAtInfinityABC):
    pass


class _DirectedLineAtInfinityABC(_LineAtInfinityABC):
    pass
