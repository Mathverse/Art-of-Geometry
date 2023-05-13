"""Entity."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Iterable, Sequence
from functools import cached_property, wraps
from inspect import (getfullargspec, getmembers,
                     isabstract, isclass, isfunction, ismethoddescriptor,
                     Parameter, signature)
from pprint import pprint
import sys
from typing import LiteralString, Optional, Self, TYPE_CHECKING

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
    def session(self: Self) -> Session:
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
    def dependencies(self: Self) -> Iterable[_EntityABC]:
        """Get dependencies."""
        if (deps := getattr(self, self._DEPENDENCIES_ATTR_KEY, None)) is None:
            setattr(self, self._DEPENDENCIES_ATTR_KEY, empty_deps := ())
            return empty_deps

        else:
            return deps

    @dependencies.setter
    def dependencies(self: Self, dependencies: Iterable[_EntityABC], /) -> None:  # noqa: E501
        """Set dependencies."""
        setattr(self, self._DEPENDENCIES_ATTR_KEY, dependencies)

    @staticmethod
    def assign_name_and_dependencies(entity_related_callable_obj: Callable, /) -> Callable:  # noqa: E501
        def decorable(function: Callable, /) -> Optional[bool]:
            assert isfunction(object=function), \
                TypeError(f'*** {function} NOT A FUNCTION ***')

            if not getattr(function, '_DECORATED_WITH_NAME_AND_DEPENDENCIES_ASSIGNMENT', False):  # noqa: E501
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
                            return (isclass(object=return_annotation_obj) and
                                    issubclass(return_annotation_obj, _EntityABC))  # noqa: E501

        def decorate(function: Callable, /, *, assign_name: bool | CallableReturningStr = True) -> Callable:
            assert isfunction(object=function), \
                TypeError(f'*** {function} NOT A FUNCTION ***')

            if debug.ON:
                print(f'DECORATING {function.__qualname__}{signature(function, follow_wrapped=False)}')
                pprint(describe(function).__dict__, sort_dicts=False)
                print('==>')

            name_already_in_arg_spec: bool = (
                'name' in getfullargspec(func=function).kwonlyargs)

            assign_name = assign_name and (not name_already_in_arg_spec)

            default_name = (assign_name
                            if isfunction(object=assign_name)
                            else None)

            @wraps(function)
            def function_with_name_and_dependencies_assignment(
                    *args,
                    name: OptionalStrOrCallableReturningStr = default_name,
                    **kwargs) \
                    -> Optional[_EntityABC]:
                dependencies: Iterable[_EntityABC] = [
                    i
                    for i in (args + tuple(kwargs.values()))
                    if isinstance(i, _EntityABC)]

                if isfunction(object=name):
                    name: str = name()

                    # validate name
                    _EntityABC._validate_name(name)

                if name_already_in_arg_spec:
                    kwargs['name']: str = name

                result = function(*args, **kwargs)

                if function.__name__ == '__new__':
                    if assign_name:
                        if isinstance(result, Symbol):
                            result.name = name

                        elif not hasattr(result, result._NAME_ATTR_KEY):
                            setattr(result, result._NAME_ATTR_KEY, name)

                    if not hasattr(result, result._DEPENDENCIES_ATTR_KEY):
                        result.dependencies: Iterable[_EntityABC] = dependencies

                    return result

                elif function.__name__ == '__init__':
                    self: _EntityABC = args[0]
                    assert isinstance(self, _EntityABC)

                    assert result is None

                    if assign_name:
                        if isinstance(self, Symbol):
                            self.name: str = name

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
                    OptionalStrOrCallableReturningStr

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
                        annotation=OptionalStrOrCallableReturningStr)

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

            if debug.ON:
                print(f'DECORATED {function_with_name_and_dependencies_assignment.__qualname__}'
                      f'{signature(function_with_name_and_dependencies_assignment)}')
                pprint(describe(function_with_name_and_dependencies_assignment).__dict__, sort_dicts=False)

            return function_with_name_and_dependencies_assignment

        if isclass(entity_related_callable_obj):
            assert issubclass(entity_related_callable_obj, _EntityABC), \
                TypeError(f'*** {entity_related_callable_obj} TO DECORATE NOT SUB-CLASS OF {_EntityABC.__name__} ***')

            assert not isabstract(entity_related_callable_obj), \
                TypeError(f'*** {entity_related_callable_obj} ABSTRACT AND NOT DECORABLE ***')

            class_members = \
                dict(getmembers(
                    entity_related_callable_obj,
                    predicate=lambda member: not (isabstract(member) or isclass(member))))

            # if __new__ is implemented somewhere in __mro__
            if isfunction(object=(__new__ := class_members.pop('__new__'))):
                entity_related_callable_obj.__new__ = \
                    decorate(
                        __new__,
                        assign_name=(True
                                     if entity_related_callable_obj._NAME_NULLABLE  # noqa: E501
                                     else UNIQUE_NAME_FACTORY))

                if debug.ON:
                    print()

            # if __init__ is implemented somewhere in __mro__
            if isfunction(object=(__init__ := class_members.pop('__init__'))):
                entity_related_callable_obj.__init__ = \
                    decorate(
                        __init__,
                        assign_name=(True
                                     if entity_related_callable_obj._NAME_NULLABLE  # noqa: E501
                                     else UNIQUE_NAME_FACTORY))

                if debug.ON:
                    print()

            else:
                assert ismethoddescriptor(object=__init__), \
                    f'??? {entity_related_callable_obj.__name__} MRO MISSING __init__ METHOD: {describe(__init__)} ???'

            for class_member_name, class_member in class_members.items():
                if isfunction(object=class_member) and decorable(class_member):
                    # Static Method
                    if is_static_method(class_member):
                        if debug.ON:
                            print(f'DECORATING STATIC METHOD {class_member.__qualname__}'
                                  f'{signature(class_member, follow_wrapped=False)}')
                            pprint(describe(class_member).__dict__, sort_dicts=False)
                            print('==>')

                        setattr(
                            entity_related_callable_obj, class_member_name,
                            staticmethod(decorate(class_member, assign_name=True)))

                        if debug.ON:
                            decorated_class_member = getattr(entity_related_callable_obj, class_member_name)

                            print('==>')
                            print(f'DECORATED STATIC METHOD {decorated_class_member.__qualname__}'
                                  f'{signature(decorated_class_member, follow_wrapped=False)}')
                            pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                            print()

                    # Unbound Instance Method
                    else:
                        assert is_instance_method(class_member, bound=False)

                        if debug.ON:
                            print(f'DECORATING UNBOUND INSTANCE METHOD {class_member.__qualname__}'
                                  f'{signature(class_member, follow_wrapped=False)}')
                            pprint(describe(class_member).__dict__, sort_dicts=False)
                            print('==>')

                        setattr(
                            entity_related_callable_obj, class_member_name,
                            decorate(class_member, assign_name=True))

                        if debug.ON:
                            decorated_class_member = getattr(entity_related_callable_obj, class_member_name)

                            print('==>')
                            print(f'DECORATED UNBOUND INSTANCE METHOD {decorated_class_member.__qualname__}'
                                  f'{signature(decorated_class_member, follow_wrapped=False)}')
                            pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                            print()

                # Class Method
                elif is_class_method(class_member) and decorable(class_member.__func__):
                    if debug.ON:
                        print(f'DECORATING CLASS METHOD {class_member.__qualname__}'
                              f'{signature(class_member, follow_wrapped=False)}')
                        pprint(describe(class_member).__dict__, sort_dicts=False)
                        print('==>')

                    setattr(
                        entity_related_callable_obj, class_member_name,
                        classmethod(decorate(class_member.__func__, assign_name=True)))

                    if debug.ON:
                        decorated_class_member = getattr(entity_related_callable_obj, class_member_name)

                        print('==>')
                        print(f'DECORATED CLASS METHOD {decorated_class_member.__qualname__}'
                              f'{signature(decorated_class_member, follow_wrapped=False)}')
                        pprint(describe(decorated_class_member).__dict__, sort_dicts=False)
                        print()

                # Cached Property
                elif isinstance(class_member, cached_property) and decorable(class_member.func):
                    if debug.ON:
                        print('DECORATING CACHED PROPERTY...')

                    setattr(
                        entity_related_callable_obj, class_member_name,
                        cached_property(decorate(class_member.func, assign_name=False)))

                    if debug.ON:
                        print()

                # Property Getter
                elif isinstance(class_member, property) and decorable(class_member.fget):
                    if debug.ON:
                        print('DECORATING PROPERTY GETTER...')

                    class_member.fget = decorate(class_member.fget, assign_name=False)

                    if debug.ON:
                        print()

            return entity_related_callable_obj

        else:
            assert isfunction(entity_related_callable_obj)

            return decorate(entity_related_callable_obj, assign_name=True)

    @classmethod
    def __class_full_name__(cls) -> str:
        return f'{cls.__module__}.{cls.__qualname__}'

    @property
    @abstractmethod
    def _short_repr(self: Self) -> str:
        raise NotImplementedError

    def __repr__(self: Self) -> str:
        return '{}{} {} {}'.format(
            f'Session "{session_name}": '
            if (session_name := self.session.name)
            else '',
            self.__class_full_name__(),
            self.name,
            f"<- ({', '.join(dependency._short_repr for dependency in dependencies)})"
            if (dependencies := self.dependencies)
            else '(FREE)')

    def __str__(self: Self) -> str:
        return repr(self)


class _GeometryEntityABC(_EntityABC, GeometryEntity):
    """Abstract Geometry Entity."""

    @property
    def name(self: Self) -> str:
        return getattr(self, self._NAME_ATTR_KEY)

    @name.setter
    def name(self: Self, name: str, /) -> None:
        # validate name
        self._validate_name(name)

        # assign name if different
        if name != getattr(self, self._NAME_ATTR_KEY):
            setattr(self, self._NAME_ATTR_KEY, name)

    @name.deleter
    def name(self: Self) -> None:
        setattr(self, self._NAME_ATTR_KEY, None)

    @abstractmethod
    def same(self: Self) -> _GeometryEntityABC:
        raise NotImplementedError

    # EQUATION & PARAMETRIC EQUATIONS
    @cached_property
    @abstractmethod
    def equation(self: Self) -> Expr:
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def parametric_equations(self: Self) -> tuple[Expr, ...]:
        raise NotImplementedError

    # INCIDENCE
    @abstractmethod
    def incident_with(self: Self, other_geometry_entity: _GeometryEntityABC) -> bool:  # noqa: E501
        """Check incidence."""
        raise NotImplementedError

    # NORMAL DIRECTION
    @abstractmethod
    def normal_direction_at_point(self: Self, point: _PointABC, /) -> _PointABC:
        raise NotImplementedError

    # alias
    def normal_direction(self: Self, point: _PointABC, /) -> _PointABC:
        return self.normal_direction_at_point(point)

    def normal(self: Self, point: _PointABC, /) -> _PointABC:
        return self.normal_direction_at_point(point)

    # PERPENDICULAR LINE
    @abstractmethod
    def perpendicular_line_at_point(self: Self, point: _PointABC, /) -> _LineABC:
        raise NotImplementedError

    # alias
    def perpendicular_line(self: Self, point: _PointABC, /) -> _LineABC:
        raise self.perpendicular_line_at_point(point)

    # TANGENT
    @abstractmethod
    def tangent_at_point(self: Self, point: _PointABC, /) -> _LinearEntityABC:
        raise NotImplementedError

    # alias
    def tangent(self: Self, point: _PointABC, /) -> _LinearEntityABC:
        return self.tangent_at_point(point)

    # CUTTING / INTERSECTION
    @abstractmethod
    def cut(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | Iterable[_GeometryEntityABC]):
        """Intersection."""
        raise NotImplementedError

    # aliases
    def intersect(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | Iterable[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def intersection(
            self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | Iterable[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def __and__(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | Iterable[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def __rand__(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | Iterable[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)
