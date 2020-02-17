from __future__ import annotations


__all__ = '_EntityABC', '_GeometryEntityABC'


from abc import abstractmethod
from functools import wraps
from inspect import isfunction
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.entity import GeometryEntity
from typing import Iterable, Optional, Tuple, TYPE_CHECKING

from ..._util._compat import cached_property
from ..._util._tmp import TMP_NAME_FACTORY
from ..._util._type import OptionalStrType


if TYPE_CHECKING:   # to avoid circular import b/w _EntityABC & Session
    from ..session import Session


class _EntityABC:
    @property
    def session(self) -> Session:
        if hasattr(self, '_session') and self._session:
            return self._session

        else:
            from ..session import DEFAULT_SESSION
            return DEFAULT_SESSION

    @session.setter
    def session(self, session: Session, /) -> None:
        from ..session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        self._session = session

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    @staticmethod
    def _with_name_assignment(_method=None, /, *, tmp_if_empty=False):
        def decorator(method, /):
            @wraps(method)
            def method_with_name_assignment(
                    cls_or_self,
                    *args,
                    name: OptionalStrType = None,
                    **kwargs) \
                    -> Optional[_EntityABC]:
                result = method(cls_or_self, *args, **kwargs)

                if tmp_if_empty and (not name):
                    name = TMP_NAME_FACTORY()

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
    def dependencies(self) -> Iterable[_EntityABC]:
        if not hasattr(self, '_dependencies'):
            self._dependencies = tuple()

        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Iterable[_EntityABC], /) -> None:
        self._dependencies = dependencies

    @staticmethod
    def _with_dependency_tracking(method, /):
        @wraps(method)
        def method_with_dependency_tracking(cls_or_self, *args, **kwargs) -> Optional[_EntityABC]:
            dependencies = \
                [i for i in args + tuple(kwargs.values())
                   if isinstance(i, _EntityABC)]

            result = method(cls_or_self, *args, **kwargs)

            if method.__name__ == '__new__':
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

        method_with_dependency_tracking._tracking_dependencies = True

        return method_with_dependency_tracking

    @staticmethod
    def _track_dependencies(Class, /):
        return Class

    @property
    @abstractmethod
    def _short_repr(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return '{}{}.{} {} {}'.format(
                f'Session "{session_name}": '
                    if (session_name := self.session.name)
                    else '',
                self.__module__,
                type(self).__name__,
                self.name,
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
    @_EntityABC._with_dependency_tracking
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
