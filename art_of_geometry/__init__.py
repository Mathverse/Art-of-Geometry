from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod

from sympy.geometry.entity import GeometryEntity


class _GeometryEntityABC(GeometryEntity):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        self._name = None

    @property
    @abstractmethod
    def equation(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)


INCIDENCE = {}
