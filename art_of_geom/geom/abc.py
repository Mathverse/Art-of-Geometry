from __future__ import annotations   # to avoid circular import b/w _GeometryEntityABC & Session


__all__ = '_GeometryEntityABC',


from abc import abstractmethod
from functools import wraps
from inspect import isfunction
from sympy.core.expr import Expr
from sympy.geometry.entity import GeometryEntity
from typing import Optional, Tuple, TYPE_CHECKING
from uuid import uuid4

from ..util.compat import cached_property


if TYPE_CHECKING:   # to avoid circular import b/w _GeometryEntityABC & Session
    from .session import Session


class _GeometryEntityABC(GeometryEntity):
    @property
    def session(self) -> Session:
        if hasattr(self, '_session') and self._session:
            return self._session

        else:
            from .session import DEFAULT_SESSION
            return DEFAULT_SESSION

    @session.setter
    def session(self, session: Session) -> None:
        from .session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        self._session = session

    @session.deleter
    def session(self) -> None:
        self._session = None

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    @staticmethod
    def _with_name_assignment(_method=None, *, uuid_if_empty=False):

        def decorator(geometry_entity_method, /):

            @wraps(geometry_entity_method)
            def geometry_entity_method_with_name_assignment(
                    cls_or_self,
                    *args,
                    name: Optional[str] = None,
                    **kwargs) \
                    -> _GeometryEntityABC:
                result = geometry_entity_method(cls_or_self, *args, **kwargs)

                if uuid_if_empty and not name:
                    name = str(uuid4())

                if geometry_entity_method.__name__ == '__new__':
                    assert result is not None
                    result._name = name
                    return result

                elif geometry_entity_method.__name__ == '__init__':
                    assert result is None
                    cls_or_self._name = name

                else:
                    assert isinstance(result, _GeometryEntityABC), \
                        TypeError(f'*** RESULT {result} NOT OF TYPE {_GeometryEntityABC.__name__} ***')
                    if name:
                        _GeometryEntityABC._validate_name(name)
                        result.name = name
                    return result

            return geometry_entity_method_with_name_assignment

        if isfunction(_method):
            return decorator(_method)
        else:
            return decorator

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str, /) -> None:
        self._validate_name(name)

        if name != self._name:
            self._name = name

    @name.deleter
    def name(self) -> None:
        self._name = None

    @property
    @abstractmethod
    def _short_repr(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.session._str_prefix}{self._short_repr}'

    def __str__(self) -> str:
        return repr(self)

    @abstractmethod
    # @_with_name_assignment   # TypeError: 'staticmethod' object is not callable
    def same(self) -> '_GeometryEntityABC':
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def equation(self) -> Expr:
        raise NotImplementedError
    
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, ...]:
        raise NotImplementedError
