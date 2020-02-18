from __future__ import annotations


__all__ = '_EntityABC', '_GeometryEntityABC'


from abc import abstractmethod
from functools import wraps
from inspect import getfullargspec, getmembers, isabstract, isclass, isfunction, ismethod, ismethoddescriptor
from logging import Handler, INFO, Logger
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.entity import GeometryEntity
import sys
from typing import Iterable, Optional, Tuple, TYPE_CHECKING

import art_of_geom._util._debug
from ..._util._compat import cached_property
from ..._util._inspect import describe
from ..._util._log import STDOUT_HANDLER, logger
from ..._util._type import OptionalStrType


if TYPE_CHECKING:   # to avoid circular import b/w _EntityABC & Session
    from ..session import Session


class _EntityABC:
    _SESSION_ATTR_KEY = '_session'

    @property
    def session(self) -> Session:
        if s := getattr(self, self._SESSION_ATTR_KEY, None):
            return s

        else:
            from ..session import DEFAULT_SESSION
            return DEFAULT_SESSION

    @session.setter
    def session(self, session: Session, /) -> None:
        from ..session import Session

        assert isinstance(session, Session), \
            TypeError(f'*** {session} NOT OF TYPE {Session.__name__} ***')

        setattr(self, self._SESSION_ATTR_KEY, session)

    _NAME_ATTR_KEY = '_name'

    @staticmethod
    def _validate_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    _DEPENDENCIES_ATTR_KEY = '_dependencies'

    @property
    def dependencies(self) -> Iterable[_EntityABC]:
        if (deps := getattr(self, self._DEPENDENCIES_ATTR_KEY, None)) is None:
            setattr(self, self._DEPENDENCIES_ATTR_KEY, empty_deps := tuple())
            return empty_deps

        else:
            return deps

    @dependencies.setter
    def dependencies(self, dependencies: Iterable[_EntityABC], /) -> None:
        setattr(self, self._DEPENDENCIES_ATTR_KEY, dependencies)

    @staticmethod
    def assign_name_and_dependencies(entity_related_obj, /):
        def decorable(function, /):
            return False \
                if getattr(function, '_DECORATED_WITH_NAME_AND_DEPENDENCIES_ASSIGNMENT', False) \
              else ((True
                     if (len(qual_name_parts := function.__qualname__.split('.')) == 2) and
                        (return_annotation == qual_name_parts[0])
                     else (isclass(return_annotation_obj := eval(return_annotation, sys.modules[function.__module__].__dict__)) and
                           issubclass(return_annotation_obj, _EntityABC)))
                    if isinstance(return_annotation := function.__annotations__.get('return'), str)
                    else False)

        def decorate(function, /):
            assert isfunction(function) \
                or ismethod(function)

            if art_of_geom._util._debug.ON:
                print(f'DECORATING {function.__qualname__}...')

            @wraps(function)
            def function_with_name_and_dependencies_assignment(
                    *args,
                    name: OptionalStrType = None,
                    **kwargs) \
                    -> Optional[_EntityABC]:
                dependencies = \
                    [i for i in (args + tuple(kwargs.values()))
                       if isinstance(i, _EntityABC)]

                name_already_in_arg_spec = ('name' in getfullargspec(function).kwonlyargs)

                if name_already_in_arg_spec:
                    kwargs['name'] = name

                possible_cls_or_self = args[0]

                try:
                    result = function(*args, **kwargs)

                except Exception:
                    # to avoid TypeError "expects N positional arguments but (N + 1) are given"
                    # when instance calls classmethod/staticmethod or when class calls staticmethod

                    assert isinstance(possible_cls_or_self, _EntityABC) \
                        or issubclass(possible_cls_or_self, _EntityABC)

                    result = function(*args[1:], **kwargs)

                to_assign_name = (not name_already_in_arg_spec)

                if function.__name__ == '__new__':
                    if to_assign_name:
                        if isinstance(result, Symbol):
                            result.name = name
                        else:
                            setattr(result, result._NAME_ATTR_KEY, name)

                    if not hasattr(result, result._DEPENDENCIES_ATTR_KEY):
                        result.dependencies = dependencies

                    return result

                elif function.__name__ == '__init__':
                    assert isinstance(possible_cls_or_self, _EntityABC)

                    assert result is None

                    if to_assign_name:
                        if isinstance(possible_cls_or_self, Symbol):
                            possible_cls_or_self.name = name
                        else:
                            setattr(possible_cls_or_self, possible_cls_or_self._NAME_ATTR_KEY, name)

                    if not hasattr(possible_cls_or_self, possible_cls_or_self._DEPENDENCIES_ATTR_KEY):
                        possible_cls_or_self.dependencies = dependencies[1:]

                else:
                    assert isinstance(result, _EntityABC), \
                        TypeError(f'*** RESULT {result} NOT OF TYPE {_EntityABC.__name__} ***')

                    if to_assign_name and name:
                        _EntityABC._validate_name(name)
                        result.name = name

                    if not hasattr(result, result._DEPENDENCIES_ATTR_KEY):
                        result.dependencies = dependencies

                    return result

            function_with_name_and_dependencies_assignment._DECORATED_WITH_NAME_AND_DEPENDENCIES_ASSIGNMENT = True

            return function_with_name_and_dependencies_assignment

        if isclass(entity_related_obj):
            assert issubclass(entity_related_obj, _EntityABC), \
                f'*** CLASS TO DECORATE MUST BE SUB-CLASS OF {_EntityABC.__name__} ***'

            assert not isabstract(entity_related_obj), \
                '*** ABSTRACT CLASSES NOT DECORATED ***'

            class_members = \
                dict(getmembers(
                        entity_related_obj,
                        predicate=lambda member: not (isabstract(member) or isclass(member))))

            __new__ = class_members.pop('__new__')
            __init__ = class_members.pop('__init__')

            if isfunction(__init__) or ismethod(__init__):
                entity_related_obj.__init__ = decorate(__init__)

            else:
                assert ismethoddescriptor(__init__), \
                    f'??? {entity_related_obj.__name__} MRO MISSING __init__ METHOD: {describe(__init__)} ???'

                if isfunction(__new__):
                    entity_related_obj.__new__ = decorate(__new__)

            for class_member_name, class_member in class_members.items():
                if (isfunction(class_member) or ismethod(class_member)) and decorable(class_member):
                    setattr(entity_related_obj, class_member_name, decorate(class_member))

                elif isinstance(class_member, cached_property) and decorable(class_member.func):
                    setattr(entity_related_obj, class_member_name, cached_property(decorate(class_member.func)))

                elif isinstance(class_member, property):
                    pass

            return entity_related_obj

        else:
            assert isfunction(entity_related_obj)
            return decorate(entity_related_obj)

    @classmethod
    def __class_full_name__(cls) -> str:
        return f'{cls.__module__}.{cls.__qualname__}'

    @classmethod
    def class_logger(cls, *handlers: Handler, level: Optional[int] = INFO) -> Logger:
        return logger(cls.__class_full_name__(), *handlers, level=level)

    @classmethod
    def class_stdout_logger(cls) -> Logger:
        return cls.class_logger(STDOUT_HANDLER)

    @property
    @abstractmethod
    def _short_repr(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return '{}{} {} {}'.format(
                f'Session "{session_name}": '
                    if (session_name := self.session.name)
                    else '',
                self.__class_full_name__(),
                self.name,
                f"<- ({', '.join(dependency._short_repr for dependency in dependencies)})"
                    if (dependencies := self.dependencies)
                    else '(FREE)')
    
    def __str__(self) -> str:
        return repr(self)

    def logger(self, *handlers: Handler, level: Optional[int] = INFO) -> Logger:
        return logger(str(self), *handlers, level=level)

    @cached_property
    def stdout_logger(self) -> Logger:
        return self.logger(STDOUT_HANDLER)


class _GeometryEntityABC(_EntityABC, GeometryEntity):
    @property
    def name(self) -> str:
        return getattr(self, self._NAME_ATTR_KEY)

    @name.setter
    def name(self, name: str, /) -> None:
        self._validate_name(name)

        if name != getattr(self, self._NAME_ATTR_KEY):
            setattr(self, self._NAME_ATTR_KEY, name)

    @name.deleter
    def name(self) -> None:
        setattr(self, self._NAME_ATTR_KEY, None)

    @abstractmethod
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
