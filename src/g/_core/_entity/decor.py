"""Decorator to assign entity name & dependencies."""


from __future__ import annotations

from functools import cached_property, wraps
from inspect import (get_annotations, getmembers,
                     isabstract, isclass, isfunction, ismethoddescriptor,
                     Parameter,
                     Signature, signature)
from pprint import pprint
import sys
from typing import TYPE_CHECKING

from sympy.core.symbol import Symbol

from g._util import debug
from g._util.inspect import (is_static_method,
                             is_class_method,
                             is_instance_method,
                             is_property,
                             is_cached_property,
                             describe)
from g._util.type import OptionalStrOrCallableReturningStr
from g._util.unique_name import UNIQUE_NAME_FACTORY

from .abc import AnEntity

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Any, LiteralString

    from g._util.type import CallableReturningStr


__all__: Sequence[LiteralString] = ('assign_entity_dependencies_and_name',)


_ALREADY_DECORATED_ATTR_KEY: LiteralString = '_DECORATED_WITH_DEPENDENCIES_AND_NAME_ASSIGNMENT'  # noqa: E501

_G_MODULE_NAME: LiteralString = 'g'

_NAME_ATTR_KEY: LiteralString = 'name'

_SELF_TYPE_STR: LiteralString = 'Self'


def _decorable(function: Callable, /) -> bool:
    """Check if function should be decorated."""
    assert isfunction(object=function), \
        TypeError(f'*** {function} NOT A FUNCTION ***')

    if (not getattr(function, _ALREADY_DECORATED_ATTR_KEY, False)) and \
            isinstance(return_annotation :=
                       signature(obj=function, follow_wrapped=True,
                                 globals=None, locals=None,
                                 eval_str=False).return_annotation, str):
        if (len(qual_name_parts :=
                function.__qualname__.split('.')) == 2) and \
                (return_annotation in (_SELF_TYPE_STR, qual_name_parts[0])):
            return True

        try:
            return_type: type = eval(return_annotation,  # noqa: S307
                                     globals=sys.modules[function.__module__].__dict__,  # noqa: E501
                                     locals=None)

        except NameError as err0:
            print(f'{function.__module__.upper()}: {err0}\n')

            try:
                return_type: type = eval(return_annotation,  # noqa: S307
                                         globals=sys.modules[_G_MODULE_NAME].__dict__,  # noqa: E501
                                         locals=None)

            except NameError as err1:
                print(f'{err1}\n')

                return False

        return (isclass(object=return_type) and issubclass(return_type, AnEntity))  # noqa: E501

    return False


def _decorate(function: Callable, /,  # noqa: C901,PLR0915
              *, assign_name: bool | CallableReturningStr = True) -> Callable:
    """Decorate function with dependencies & name assignment."""
    assert isfunction(object=function), \
        TypeError(f'*** {function} NOT A FUNCTION ***')

    if debug.ON:
        print(f'DECORATING {function.__qualname__}'
              f'{signature(obj=function, follow_wrapped=False, eval_str=True)}')  # noqa: E501
        pprint(object=describe(function).__dict__,
               stream=None,
               indent=2,
               width=80,
               depth=None,
               compact=False,
               sort_dicts=False,
               underscore_numbers=False)
        print('==>')

    name_already_in_arg_spec: bool = _NAME_ATTR_KEY in signature(obj=function).parameters  # noqa: E501

    assign_name: bool | CallableReturningStr = \
        assign_name and (not name_already_in_arg_spec)

    default_name: CallableReturningStr | None = (assign_name
                                                 if isfunction(object=assign_name)  # noqa: E501
                                                 else None)

    @wraps(wrapped=function)
    def function_with_dependencies_and_name_assignment(  # noqa: C901
            *args: Any,
            name: OptionalStrOrCallableReturningStr = default_name,
            **kwargs: Any) -> AnEntity | None:
        dependencies: set[AnEntity] = {i
                                       for i in (args + tuple(kwargs.values()))
                                       if isinstance(i, AnEntity)}

        if isfunction(object=name):
            name: str = name()

            # validate name
            AnEntity._validate_name(name)

        if name_already_in_arg_spec:
            kwargs[_NAME_ATTR_KEY]: str = name

        result: AnEntity | None = function(*args, **kwargs)

        if function.__name__ == '__new__':
            # assign dependencies
            if not hasattr(result, result._DEPS_ATTR_KEY):
                result.dependencies: set[AnEntity] = dependencies

            # assign name
            if assign_name:
                if isinstance(result, Symbol):
                    result.name: str = name

                elif not hasattr(result, result._NAME_ATTR_KEY):  # noqa: E501,RUF100
                    setattr(result, result._NAME_ATTR_KEY, name)  # noqa: E501,RUF100

            return result

        if function.__name__ == '__init__':
            self: AnEntity = args[0]
            assert isinstance(self, AnEntity)

            assert result is None

            # assign dependencies
            if not hasattr(self, self._DEPS_ATTR_KEY):
                self.dependencies: set[AnEntity] = dependencies[1:]

            # assign name
            if assign_name:
                if isinstance(self, Symbol):
                    self.name: str = name

                elif not hasattr(self, self._NAME_ATTR_KEY):
                    setattr(self, self._NAME_ATTR_KEY, name)

            return None

        assert isinstance(result, AnEntity), \
            TypeError(f'*** RESULT {result} NOT OF TYPE {AnEntity.__name__} ***')  # noqa: E501

        # assign dependencies
        if not hasattr(result, result._DEPS_ATTR_KEY):
            result.dependencies: set[AnEntity] = dependencies

        # assign name
        if assign_name and name:
            # validate name
            AnEntity._validate_name(name)

            result.name: str = name

        return result

    function_with_dependencies_and_name_assignment._DECORATED_WITH_DEPENDENCIES_AND_NAME_ASSIGNMENT: bool = True  # noqa: E501

    if not name_already_in_arg_spec:
        function_with_dependencies_and_name_assignment.__annotations__[
            _NAME_ATTR_KEY] = OptionalStrOrCallableReturningStr

        function_signature: Signature = \
            signature(function, follow_wrapped=False)

        function_parameters: list[Any] = \
            list(function_signature.parameters.values())

        name_parameter: Parameter = \
            Parameter(name=_NAME_ATTR_KEY,
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
            function_parameters.insert(kwargs_parameter_index,
                                       name_parameter)

        function_with_dependencies_and_name_assignment.__signature__ = (
            function_signature.replace(parameters=function_parameters))

    if debug.ON:
        print(f'DECORATED {function_with_dependencies_and_name_assignment.__qualname__}'  # noqa: E501
              f'{signature(function_with_dependencies_and_name_assignment)}')
        pprint(describe(function_with_dependencies_and_name_assignment).__dict__,  # noqa: E501,RUF100
               sort_dicts=False)

    return function_with_dependencies_and_name_assignment


def assign_entity_dependencies_and_name(entity_related_callable: Callable, /) -> Callable:  # noqa: C901,E501,PLR0915
    """Assign Name & Dependencies to Newly-Created Entity."""
    if isclass(object=entity_related_callable):
        assert issubclass(entity_related_callable, AnEntity), \
            TypeError(f'*** {entity_related_callable} TO DECORATE '
                      f'NOT SUB-CLASS OF {AnEntity.__name__} ***')

        assert not isabstract(entity_related_callable), \
            TypeError(f'*** {entity_related_callable} ABSTRACT '
                      'AND NOT _decorable( ***')

        class_members: dict[LiteralString, Any] = \
            dict(getmembers(object=entity_related_callable,
                            predicate=lambda member: not (isabstract(object=member) or  # noqa: E501
                                                          isclass(object=member))))  # noqa: E501,RUF100

        # if __new__ is implemented somewhere in __mro__
        if isfunction(object=(__new__ := class_members.pop('__new__'))):
            entity_related_callable.__new__: Callable[..., AnEntity] = \
                _decorate(__new__,
                          assign_name=(True
                                       if entity_related_callable._NAME_NULLABLE  # noqa: E501
                                       else UNIQUE_NAME_FACTORY))

            if debug.ON:
                print()

        # if __init__ is implemented somewhere in __mro__
        if isfunction(object=(__init__ := class_members.pop('__init__'))):
            entity_related_callable.__init__: Callable[..., None] = \
                _decorate(__init__,
                          assign_name=(True
                                       if entity_related_callable._NAME_NULLABLE  # noqa: E501
                                       else UNIQUE_NAME_FACTORY))

            if debug.ON:
                print()

        else:
            assert ismethoddescriptor(object=__init__), \
                (f'??? {entity_related_callable.__name__} MRO '
                 f'MISSING __init__ METHOD: {describe(__init__)} ???')

        for class_member_name, class_member in class_members.items():
            if isfunction(object=class_member) and _decorable(class_member):
                # Static Method
                if is_static_method(class_member):
                    if debug.ON:
                        print(f'DECORATING STATIC METHOD {class_member.__qualname__}'  # noqa: E501
                              f'{signature(class_member, follow_wrapped=False)}')  # noqa: E501
                        pprint(describe(class_member).__dict__,
                               sort_dicts=False)
                        print('==>')

                    setattr(entity_related_callable, class_member_name,
                            staticmethod(_decorate(class_member,
                                                   assign_name=True)))

                    if debug.ON:
                        decorated_class_member = \
                            getattr(entity_related_callable,
                                    class_member_name)

                        print('==>')
                        print(f'DECORATED STATIC METHOD {decorated_class_member.__qualname__}'  # noqa: E501
                              f'{signature(decorated_class_member, follow_wrapped=False)}')  # noqa: E501
                        pprint(describe(decorated_class_member).__dict__,
                               sort_dicts=False)
                        print()

                # Unbound Instance Method
                else:
                    assert is_instance_method(class_member, bound=False)

                    if debug.ON:
                        print(f'DECORATING UNBOUND INSTANCE METHOD {class_member.__qualname__}'  # noqa: E501
                              f'{signature(class_member, follow_wrapped=False)}')  # noqa: E501
                        pprint(describe(class_member).__dict__,
                               sort_dicts=False)
                        print('==>')

                    setattr(entity_related_callable, class_member_name,
                            _decorate(class_member, assign_name=True))

                    if debug.ON:
                        decorated_class_member = \
                            getattr(entity_related_callable,
                                    class_member_name)

                        print('==>')
                        print(f'DECORATED UNBOUND INSTANCE METHOD {decorated_class_member.__qualname__}'  # noqa: E501
                              f'{signature(decorated_class_member, follow_wrapped=False)}')  # noqa: E501
                        pprint(describe(decorated_class_member).__dict__,
                               sort_dicts=False)
                        print()

            # Class Method
            elif is_class_method(class_member) and _decorable(class_member.__func__):  # noqa: E501
                if debug.ON:
                    print(f'DECORATING CLASS METHOD {class_member.__qualname__}'  # noqa: E501
                          f'{signature(class_member, follow_wrapped=False)}')
                    pprint(describe(class_member).__dict__,
                           sort_dicts=False)
                    print('==>')

                setattr(entity_related_callable, class_member_name,
                        classmethod(_decorate(class_member.__func__,
                                              assign_name=True)))

                if debug.ON:
                    decorated_class_member = \
                        getattr(entity_related_callable,
                                class_member_name)

                    print('==>')
                    print(f'DECORATED CLASS METHOD {decorated_class_member.__qualname__}'  # noqa: E501
                          f'{signature(decorated_class_member, follow_wrapped=False)}')  # noqa: E501
                    pprint(describe(decorated_class_member).__dict__,
                           sort_dicts=False)
                    print()

            # Property's Underlying Getter Function
            elif is_property(class_member):
                if debug.ON:
                    print("DECORATING INSTANCE PROPERTY'S GETTER FUNCTION...")

                class_member.fget: Callable = _decorate(class_member.fget,
                                                        assign_name=False)

                if debug.ON:
                    print()

            # Cached Property's Underlying Function
            elif is_cached_property(class_member):
                if debug.ON:
                    print("DECORATING INSTANCE CACHED PROPERTY'S "
                          'UNDERLYING FUNCTION...')

                setattr(entity_related_callable, class_member_name,
                        cached_property(_decorate(class_member.func,
                                                  assign_name=False)))

                if debug.ON:
                    print()

        return entity_related_callable

    return _decorate(entity_related_callable, assign_name=True)
