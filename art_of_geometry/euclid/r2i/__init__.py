from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod

from ... import _GeometryEntityABC


class _SurfaceInR2IABC(_GeometryEntityABC):
    @property
    @abstractmethod
    def equation(self):
        raise NotImplementedError
