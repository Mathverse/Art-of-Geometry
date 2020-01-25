__all__ = '_GeometryEntityABC',


from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from functools import cached_property
from sympy.core.expr import Expr
from sympy.geometry.entity import GeometryEntity
from typing import Tuple


class _GeometryEntityABC(GeometryEntity):
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @name.deleter
    def name(self) -> None:
        self._name = None

    def __str__(self) -> str:
        return repr(self)

    @abstractmethod
    def same(self, *, name=None):
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def equation(self) -> Expr:
        raise NotImplementedError
    
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, ...]:
        raise NotImplementedError
