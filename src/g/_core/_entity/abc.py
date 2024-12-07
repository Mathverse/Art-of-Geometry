"""Abstract Entity."""


from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self

    from g.session import Session


__all__: Sequence[LiteralString] = ('AnEntity',)


class AnEntity:
    """Abstract Entity."""

    _SESS_ATTR_KEY: LiteralString = '_session'

    @property
    def session(self: Self, /) -> Session:
        if s := getattr(self, self._SESS_ATTR_KEY, None):
            return s

        else:
            from g.session import DEFAULT_SESSION

            setattr(self, self._SESS_ATTR_KEY, DEFAULT_SESSION)

            return DEFAULT_SESSION

    @session.setter
    def session(self: Self, session: Session, /) -> None:
        from g.session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        setattr(self, self._SESS_ATTR_KEY, session)

    _DEPS_ATTR_KEY: LiteralString = '_dependencies'

    @property
    def dependencies(self: Self, /) -> set[AnEntity]:
        """Get dependencies."""
        if (deps := getattr(self, self._DEPS_ATTR_KEY, None)) is None:
            setattr(self, self._DEPS_ATTR_KEY, empty_deps := set[AnEntity]())
            return empty_deps

        else:
            return deps

    @dependencies.setter
    def dependencies(self: Self, dependencies: set[AnEntity], /) -> None:
        """Set dependencies."""
        setattr(self, self._DEPS_ATTR_KEY, dependencies)

    _NAME_ATTR_KEY: LiteralString = '_name'
    _NAME_NULLABLE: bool = True

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

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
        return ((f'Session "{sess_name}": '
                 if (sess_name := self.session.name)
                 else '') +
                f'{self.__class_full_name__()} {self.name} ' +
                (f"<- ({', '.join(dep._short_repr for dep in deps)})"
                 if (deps := self.dependencies)
                 else '(FREE)'))

    def __str__(self: Self, /) -> str:
        """Return string representation."""
        return repr(self)
