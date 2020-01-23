from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod

from ... import _GeometryEntityABC


class _EuclidR2GeometryEntityABC(_GeometryEntityABC):
    @property
    @abstractmethod
    def equation(self):
        raise NotImplementedError
