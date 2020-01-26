__all__ = '_GeometryEntityABC',


from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from functools import cached_property
from sympy.core.expr import Expr
from sympy.geometry.entity import GeometryEntity
from typing import Tuple
from uuid import uuid4


class _GeometryEntityABC(GeometryEntity):
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str, /) -> None:
        if name != self._name:
            assert isinstance(name, str) and name, \
                TypeError(
                    '*** {} NOT NON-EMPTY STRING ***'
                    .format(name))

            self._name = name

    @name.deleter
    def name(self) -> None:
        self.name = str(uuid4())

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
