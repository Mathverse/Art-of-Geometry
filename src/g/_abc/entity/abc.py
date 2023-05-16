"""Abstract Entity."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from functools import cache
from typing import LiteralString, Self, TYPE_CHECKING

if TYPE_CHECKING:  # avoid circular import between _EntityABC & Session
    from ...session import Session


__all__: Sequence[LiteralString] = ('_EntityABC',)


class _EntityABC:
    """Abstract Entity."""

    _SESSION_ATTR_KEY: LiteralString = '_session'

    @property
    def session(self: Self, /) -> Session:
        if s := getattr(self, self._SESSION_ATTR_KEY, None):
            return s

        else:
            from ..session import DEFAULT_SESSION

            setattr(self, self._SESSION_ATTR_KEY, DEFAULT_SESSION)

            return DEFAULT_SESSION

    @session.setter
    def session(self: Self, session: Session, /) -> None:
        from ...session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        setattr(self, self._SESSION_ATTR_KEY, session)

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

    _NAME_ATTR_KEY: LiteralString = '_name'
    _NAME_NULLABLE: bool = True

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    @cache
    @classmethod
    def __class_full_name__(cls: type, /) -> LiteralString:
        return f'{cls.__module__}.{cls.__qualname__}'

    @property
    @abstractmethod
    def _short_repr(self: Self, /) -> str:
        """Return short string representation."""
        raise NotImplementedError

    def __repr__(self: Self, /) -> str:
        """Return string representation."""
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
        """Return string representation."""
        return repr(self)
