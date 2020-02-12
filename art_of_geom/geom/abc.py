__all__ = '_GeometryEntityABC',


from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from sympy.core.expr import Expr
from sympy.geometry.entity import GeometryEntity
from typing import Optional, Tuple

from ..util.compat import cached_property
# from .session import Session, GLOBAL_SESSION   # import within the class below instead to avoid circular importing


class _GeometryEntityABC(GeometryEntity):
    from .session import Session

    @property
    def session(self) -> Session:
        if hasattr(self, '_session') and self._session:
            return self._session

        else:
            from .session import GLOBAL_SESSION
            return GLOBAL_SESSION

    @session.setter
    def session(self, session: Session) -> None:
        from .session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        self._session = session

    @session.deleter
    def session(self) -> None:
        self._session = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str, /) -> None:
        if name != self._name:
            assert isinstance(name, str) and name, \
                TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

            self._name = name

    @name.deleter
    def name(self) -> None:
        self._name = None

    def __str__(self) -> str:
        return repr(self)

    @abstractmethod
    def same(self, /, *, name: Optional[str] = None) -> '_GeometryEntityABC':
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def equation(self) -> Expr:
        raise NotImplementedError
    
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, ...]:
        raise NotImplementedError
