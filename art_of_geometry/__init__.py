from abc import ABC, ABCMeta, abstractmethod, abstractproperty

from sympy.geometry.entity import GeometryEntity


class _GeometryEntityABC(GeometryEntity, ABC):
    @abstractmethod
    @property
    def name(self):
        raise NotImplementedError

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        self._name = None

    def __str__(self):
        return repr(self)
