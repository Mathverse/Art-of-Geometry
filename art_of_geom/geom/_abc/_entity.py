from __future__ import annotations


__all__ = '_EntityABC', '_GeometryEntityABC'


from abc import abstractmethod
from functools import wraps
from inspect import \
    getfullargspec, getmembers, \
    isabstract, isclass, isfunction, ismethod, ismethoddescriptor, \
    Parameter, signature
from logging import Handler, INFO, Logger
from pprint import pprint
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.entity import GeometryEntity
import sys
from typing import Callable, Iterable, Optional, Tuple, TYPE_CHECKING, Union

import art_of_geom._util._debug
from ..._util._compat import cached_property
from ..._util._inspect import is_static_method, is_class_method, is_special_op, describe
from ..._util._log import STDOUT_HANDLER, logger
from ..._util._tmp import TMP_NAME_FACTORY
from ..._util._type import CallableReturningStrType, OptionalStrOrCallableReturningStrType


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
    _NAME_NULLABLE = True

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
    def assign_name_and_dependencies(entity_related_obj: Callable, /) -> Callable:
        def decorable(function: Callable, /) -> Optional[bool]:
            assert isfunction(function) or ismethod(function), \
                f'*** {function} NEITHER FUNCTION NOR METHOD ***'

            if not getattr(function, '_DECORATED_WITH_NAME_AND_DEPENDENCIES_ASSIGNMENT', False):
                if isinstance(return_annotation := function.__annotations__.get('return'), str):
                    if (len(qual_name_parts := function.__qualname__.split('.')) == 2) and \
                            (return_annotation == qual_name_parts[0]):
                        return True

                    else:
                        try:
                            return_annotation_obj = \
                                eval(return_annotation,
                                     sys.modules[function.__module__].__dict__)

                        except NameError:
                            return False

                        else:
                            return isclass(return_annotation_obj) \
                               and issubclass(return_annotation_obj, _EntityABC)

        def decorate(function: Callable, /, *, assign_name: Union[bool, CallableReturningStrType] = True) -> Callable:
            assert isfunction(function) or ismethod(function), \
                f'*** {function} NEITHER FUNCTION NOR METHOD ***'

            if art_of_geom._util._debug.ON:
                print(f'DECORATING {function.__qualname__}{signature(function, follow_wrapped=False)}')
                pprint(describe(function).__dict__, sort_dicts=False)
                print('==>')

            name_already_in_arg_spec = ('name' in getfullargspec(function).kwonlyargs)

            assign_name = assign_name and (not name_already_in_arg_spec)

            default_name = \
                assign_name \
                if isfunction(assign_name) \
                else None

            @wraps(function)
            def function_with_name_and_dependencies_assignment(
                    *args,
                    name: OptionalStrOrCallableReturningStrType = default_name,
                    **kwargs) \
                    -> Optional[_EntityABC]:
                dependencies = \
                    [i for i in (args + tuple(kwargs.values()))
                       if isinstance(i, _EntityABC)]

                if isfunction(name):
                    name = name()
                    _EntityABC._validate_name(name)

                if name_already_in_arg_spec:
                    kwargs['name'] = name

                result = function(*args, **kwargs)

                if function.__name__ == '__new__':
                    if assign_name:
                        if isinstance(result, Symbol):
                            result.name = name

                        elif not hasattr(result, result._NAME_ATTR_KEY):
                            setattr(result, result._NAME_ATTR_KEY, name)

                    if not hasattr(result, result._DEPENDENCIES_ATTR_KEY):
                        result.dependencies = dependencies

                    return result

                elif function.__name__ == '__init__':
                    self = args[0]
                    assert isinstance(self, _EntityABC)

                    assert result is None

                    if assign_name:
                        if isinstance(self, Symbol):
                            self.name = name

                        elif not hasattr(self, self._NAME_ATTR_KEY):
                            setattr(self, self._NAME_ATTR_KEY, name)

                    if not hasattr(self, self._DEPENDENCIES_ATTR_KEY):
                        self.dependencies = dependencies[1:]

                else:
                    assert isinstance(result, _EntityABC), \
                        TypeError(f'*** RESULT {result} NOT OF TYPE {_EntityABC.__name__} ***')

                    if assign_name and name:
                        _EntityABC._validate_name(name)
                        result.name = name

                    if not hasattr(result, result._DEPENDENCIES_ATTR_KEY):
                        result.dependencies = dependencies

                    return result

            function_with_name_and_dependencies_assignment._DECORATED_WITH_NAME_AND_DEPENDENCIES_ASSIGNMENT = True

            if not name_already_in_arg_spec:
                function_with_name_and_dependencies_assignment.__annotations__['name'] = \
                    OptionalStrOrCallableReturningStrType

                function_signature = \
                    signature(
                        function_with_name_and_dependencies_assignment,
                        follow_wrapped=True)

                function_parameters = list(function_signature.parameters.values())

                name_parameter = \
                    Parameter(
                        name='name',
                        kind=Parameter.KEYWORD_ONLY,
                        default=default_name,
                        annotation=OptionalStrOrCallableReturningStrType)

                try:
                    kwargs_parameter_index = \
                        next(i
                             for i, parameter in enumerate(function_parameters)
                             if parameter.kind == Parameter.VAR_KEYWORD)

                except StopIteration:
                    function_parameters.append(name_parameter)

                else:
                    function_parameters.insert(kwargs_parameter_index, name_parameter)

                function_with_name_and_dependencies_assignment.__signature__ = \
                    function_signature.replace(parameters=function_parameters)

            if art_of_geom._util._debug.ON:
                print(f'DECORATED {function_with_name_and_dependencies_assignment.__qualname__}'
                      f'{signature(function_with_name_and_dependencies_assignment)}')
                pprint(describe(function_with_name_and_dependencies_assignment).__dict__, sort_dicts=False)

            return function_with_name_and_dependencies_assignment

        if isclass(entity_related_obj):
            assert issubclass(entity_related_obj, _EntityABC), \
                f'*** {entity_related_obj} TO DECORATE NOT SUB-CLASS OF {_EntityABC.__name__} ***'

            assert not isabstract(entity_related_obj), \
                f'*** {entity_related_obj} ABSTRACT AND NOT DECORABLE ***'

            class_members = \
                dict(getmembers(
                        entity_related_obj,
                        predicate=lambda member: not (isabstract(member) or isclass(member))))

            # if __new__ is implemented somewhere in __mro__
            if isfunction(__new__ := class_members.pop('__new__')):
                entity_related_obj.__new__ = \
                    decorate(
                        __new__,
                        assign_name=
                            True
                            if entity_related_obj._NAME_NULLABLE
                            else TMP_NAME_FACTORY)

                if art_of_geom._util._debug.ON:
                    print()

            # if __init__ is implemented somewhere in __mro__
            if isfunction(__init__ := class_members.pop('__init__')):
                entity_related_obj.__init__ = \
                    decorate(
                        __init__,
                        assign_name=
                            True
                            if entity_related_obj._NAME_NULLABLE
                            else TMP_NAME_FACTORY)

                if art_of_geom._util._debug.ON:
                    print()

            else:
                assert ismethoddescriptor(__init__), \
                    f'??? {entity_related_obj.__name__} MRO MISSING __init__ METHOD: {describe(__init__)} ???'

            for class_member_name, class_member in class_members.items():
                if isfunction(class_member) and decorable(class_member):
                    # Static Method
                    if is_static_method(class_member):
                        if art_of_geom._util._debug.ON:
                            print(f'DECORATING STATIC METHOD {class_member.__qualname__}'
                                  f'{signature(class_member, follow_wrapped=False)}')
                            pprint(describe(class_member).__dict__, sort_dicts=False)
                            print('==>')

                        setattr(
                            entity_related_obj, class_member_name,
                            staticmethod(decorate(class_member, assign_name=True)))

                        if art_of_geom._util._debug.ON:
                            decorated_class_member = getattr(entity_related_obj, class_member_name)

                            print('==>')
                            print(f'DECORATED STATIC METHOD {decorated_class_member.__qualname__}'
                                  f'{signature(decorated_class_member, follow_wrapped=False)}')
                            pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                            print()

                    # __special_operator__
                    elif is_special_op(class_member):
                        if art_of_geom._util._debug.ON:
                            print(f'DECORATING SPECIAL OPERATOR {class_member.__qualname__}'
                                  f'{signature(class_member, follow_wrapped=False)}')
                            pprint(describe(class_member).__dict__, sort_dicts=False)
                            print('==>')

                        setattr(
                            entity_related_obj, class_member_name,
                            decorate(class_member, assign_name=True))   # TODO: consider if False is more appropriate

                        if art_of_geom._util._debug.ON:
                            decorated_class_member = getattr(entity_related_obj, class_member_name)

                            print('==>')
                            print(f'DECORATED SPECIAL OPERATOR {decorated_class_member.__qualname__}'
                                  f'{signature(decorated_class_member, follow_wrapped=False)}')
                            pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                            print()

                    # Instance Method
                    else:
                        if art_of_geom._util._debug.ON:
                            print(f'DECORATING INSTANCE METHOD {class_member.__qualname__}'
                                  f'{signature(class_member, follow_wrapped=False)}')
                            pprint(describe(class_member).__dict__, sort_dicts=False)
                            print('==>')

                        setattr(
                            entity_related_obj, class_member_name,
                            decorate(class_member, assign_name=True))

                        if art_of_geom._util._debug.ON:
                            decorated_class_member = getattr(entity_related_obj, class_member_name)

                            print('==>')
                            print(f'DECORATED INSTANCE METHOD {decorated_class_member.__qualname__}'
                                  f'{signature(decorated_class_member, follow_wrapped=False)}')
                            pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                            print()

                # Class Method
                elif is_class_method(class_member) and decorable(class_member.__func__):
                    if art_of_geom._util._debug.ON:
                        print(f'DECORATING CLASS METHOD {class_member.__qualname__}'
                              f'{signature(class_member, follow_wrapped=False)}')
                        pprint(describe(class_member).__dict__, sort_dicts=False)
                        print('==>')

                    setattr(
                        entity_related_obj, class_member_name,
                        classmethod(decorate(class_member.__func__, assign_name=True)))

                    if art_of_geom._util._debug.ON:
                        decorated_class_member = getattr(entity_related_obj, class_member_name)

                        print('==>')
                        print(f'DECORATED CLASS METHOD {decorated_class_member.__qualname__}'
                              f'{signature(decorated_class_member, follow_wrapped=False)}')
                        pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                        print()

                # Cached Property
                elif isinstance(class_member, cached_property) and decorable(class_member.func):
                    if art_of_geom._util._debug.ON:
                        print('DECORATING CACHED PROPERTY...')

                    setattr(
                        entity_related_obj, class_member_name,
                        cached_property(decorate(class_member.func, assign_name=False)))

                    if art_of_geom._util._debug.ON:
                        print()

                # Property Getter
                elif isinstance(class_member, property) and decorable(class_member.fget):
                    if art_of_geom._util._debug.ON:
                        print('DECORATING PROPERTY GETTER...')

                    class_member.fget = decorate(class_member.fget, assign_name=False)

                    if art_of_geom._util._debug.ON:
                        print()

            return entity_related_obj

        else:
            assert isfunction(entity_related_obj)

            return decorate(entity_related_obj, assign_name=True)

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
