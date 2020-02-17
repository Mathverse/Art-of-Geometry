from __future__ import annotations


__all__ = '_EntityABC', '_GeometryEntityABC'


from abc import abstractmethod
from functools import wraps
from inspect import isfunction
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.entity import GeometryEntity
from typing import Optional, Tuple, TYPE_CHECKING
from uuid import uuid4

from ..util.compat import cached_property
from ..util.types import OptionalStrType


if TYPE_CHECKING:   # to avoid circular import b/w _GeometryEntityABC & Session
    from .session import Session


class _EntityABC:
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

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    @staticmethod
    def _with_name_assignment(_method=None, *, uuid_if_empty=False):

        def decorator(method, /):

            @wraps(method)
            def method_with_name_assignment(
                    cls_or_self,
                    *args,
                    name: OptionalStrType = None,
                    **kwargs) \
                    -> Optional[_EntityABC]:
                result = method(cls_or_self, *args, **kwargs)

                if uuid_if_empty and not name:
                    name = str(uuid4())

                if method.__name__ == '__new__':
                    if isinstance(result, Symbol):
                        result.name = name
                    else:
                        result._name = name
                    return result

                elif method.__name__ == '__init__':
                    assert result is None
                    cls_or_self._name = name

                else:
                    assert isinstance(result, _EntityABC), \
                        TypeError(f'*** RESULT {result} NOT OF TYPE {_EntityABC.__name__} ***')
                    if name:
                        _EntityABC._validate_name(name)
                        result.name = name
                    return result

            return method_with_name_assignment

        return decorator(_method) \
            if isfunction(_method) \
          else decorator

    @property
    def dependencies(self) -> Tuple[_EntityABC]:
        if not hasattr(self, '_dependencies'):
            self._dependencies = tuple()

        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Tuple[_EntityABC]) -> None:
        self._dependencies = dependencies

    @staticmethod
    def _with_dependency_tracking(method):
        @wraps(method)
        def method_with_dependency_tracking(cls_or_self, *args, **kwargs) -> Optional[_EntityABC]:
            dependencies = \
                [i for i in args + tuple(kwargs.values())
                   if isinstance(i, _EntityABC)]

            result = method(cls_or_self, *args, **kwargs)

            if method.__name__ == '__new__':
                assert result is not None
                result.dependencies = dependencies
                return result

            elif method.__name__ == '__init__':
                assert result is None
                cls_or_self.dependencies = dependencies

            else:
                assert isinstance(result, _EntityABC), \
                    TypeError(f'*** RESULT {result} NOT OF TYPE {_EntityABC.__name__} ***')
                result.dependencies = dependencies
                return result

        return method_with_dependency_tracking

    @property
    @abstractmethod
    def _short_repr(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.session._str_prefix}{self.__module__} {self._short_repr}"' {}'.format(
                f"<- ({', '.join(dependency._short_repr for dependency in dependencies)})"
                if (dependencies := self.dependencies)
                else '(FREE)')
    
    def __str__(self) -> str:
        return repr(self)


class _GeometryEntityABC(_EntityABC, GeometryEntity):
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

    @abstractmethod
    @_EntityABC._with_name_assignment
    def same(self) -> _GeometryEntityABC:
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def equation(self) -> Expr:
        raise NotImplementedError
    
    @cached_property
    @abstractmethod
    def parametric_equations(self) -> Tuple[Expr, ...]:
        raise NotImplementedError
