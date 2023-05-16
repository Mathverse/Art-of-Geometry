"""Abstract Entity."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Sequence
from functools import cached_property, wraps
from inspect import (getmembers,
                     isabstract, isclass, isfunction, ismethoddescriptor,
                     Parameter, signature)
from pprint import pprint
import sys
from typing import Any, LiteralString, Optional, Self, TYPE_CHECKING

from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.entity import GeometryEntity

from .._util import debug
from .._util.inspect import is_static_method, is_class_method, is_instance_method, describe  # noqa: E501
from .._util.type import CallableReturningStr, OptionalStrOrCallableReturningStr  # noqa: E501
from .._util.unique_name import UNIQUE_NAME_FACTORY

if TYPE_CHECKING:  # avoid circular import between _EntityABC & Session
    from .session import Session
    from .point import _PointABC
    from .line import _LinearEntityABC, _LineABC


__all__: Sequence[LiteralString] = '_EntityABC', '_GeometryEntityABC'


class _EntityABC:
    """Abstract Entity."""

    _SESSION_ATTR_KEY: LiteralString = '_session'

    @property
    def session(self: Self, /) -> Session:
        if s := getattr(self, self._SESSION_ATTR_KEY, None):
            return s

        else:
            from .session import DEFAULT_SESSION
            return DEFAULT_SESSION

    @session.setter
    def session(self: Self, session: Session, /) -> None:
        from .session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        setattr(self, self._SESSION_ATTR_KEY, session)

    _NAME_ATTR_KEY: LiteralString = '_name'
    _NAME_NULLABLE: bool = True

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    _DEPENDENCIES_ATTR_KEY: LiteralString = '_dependencies'

    @property
    def dependencies(self: Self, /) -> set[_EntityABC]:
        """Get dependencies."""
        if (deps := getattr(self, self._DEPENDENCIES_ATTR_KEY, None)) is None:
            setattr(self, self._DEPENDENCIES_ATTR_KEY, empty_deps := set[_EntityABC]())  # noqa: E501
            return empty_deps

        else:
            return deps

    @dependencies.setter
    def dependencies(self: Self, dependencies: set[_EntityABC], /) -> None:
        """Set dependencies."""
        setattr(self, self._DEPENDENCIES_ATTR_KEY, dependencies)

    @classmethod
    def __class_full_name__(cls, /) -> str:
        return f'{cls.__module__}.{cls.__qualname__}'

    @property
    @abstractmethod
    def _short_repr(self: Self, /) -> str:
        raise NotImplementedError

    def __repr__(self: Self, /) -> str:
        return '{}{} {} {}'.format(
            f'Session "{session_name}": '
            if (session_name := self.session.name)
            else '',
            self.__class_full_name__(),
            self.name,
            f"<- ({', '.join(dependency._short_repr for dependency in dependencies)})"  # noqa: E501
            if (dependencies := self.dependencies)
            else '(FREE)')

    def __str__(self: Self, /) -> str:
        return repr(self)
