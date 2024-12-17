"""Decorator to assign entity name & dependencies."""


from __future__ import annotations

from functools import cached_property, wraps
from inspect import (getmembers,
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


_SELF_TYPE_STR: LiteralString = 'Self'

_G_MODULE_NAME: LiteralString = 'g'

_NEW_METHOD_NAME: LiteralString = '__new__'
_INIT_METHOD_NAME: LiteralString = '__init__'

_ALREADY_DECORATED_ATTR_KEY: LiteralString = '_DECORATED_WITH_DEPENDENCIES_AND_NAME_ASSIGNMENT'  # noqa: E501
_NAME_ATTR_KEY: LiteralString = 'name'


def _decorable(function: Callable, /) -> bool:
    """Check if function should be decorated."""
    assert isfunction(object=function), \
        TypeError(f'*** {function} NOT A FUNCTION ***')

    if (not getattr(function, _ALREADY_DECORATED_ATTR_KEY, False)) and \
            isinstance(return_annotation :=
                       signature(obj=function, follow_wrapped=False,
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
            if debug.ON:
                print(f'{function.__module__.upper()}: {err0}\n')

            try:
                return_type: type = eval(return_annotation,  # noqa: S307
                                         globals=sys.modules[_G_MODULE_NAME].__dict__,  # noqa: E501
                                         locals=None)

            except NameError as err1:
                if debug.ON:
                    print(f'{err1}\n')

                return False

        return (isclass(object=return_type) and issubclass(return_type, AnEntity))  # noqa: E501

    return False


def _func_qualname_and_signature(function: Callable, /) -> str:
    return f'{function.__qualname__}{signature(obj=function,
                                               follow_wrapped=False,
                                               globals=None, locals=None,
                                               eval_str=False)}'


def _decorate(function: Callable, /,  # noqa: C901,PLR0915
              *, assign_name: bool | CallableReturningStr = True) -> Callable:
    """Decorate function with dependencies & name assignment."""
    assert isfunction(object=function), \
        TypeError(f'*** {function} NOT A FUNCTION ***')

    if debug.ON:
        print(f'DECORATING {_func_qualname_and_signature(function)}')
        pprint(object=describe(function).__dict__,
               stream=None,
               indent=2,
               width=80,
               depth=None,
               compact=False,
               sort_dicts=False,
               underscore_numbers=False)
        print('==>')

    assign_name |= not (name_already_in_arg_spec :=
                        (_NAME_ATTR_KEY in signature(obj=function,
                                                     follow_wrapped=False,
                                                     globals=None, locals=None,
                                                     eval_str=False).parameters))  # noqa: E501

    default_name_factory: CallableReturningStr | None = (assign_name
                                                         if isfunction(object=assign_name)  # noqa: E501
                                                         else None)

    @wraps(wrapped=function)
    def func_w_deps_and_name_assignment(  # noqa: C901
            *args: Any,
            name: OptionalStrOrCallableReturningStr = default_name_factory,
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

        if function.__name__ == _NEW_METHOD_NAME:
            # assign dependencies
            if not hasattr(result, result._DEPS_ATTR_KEY):
                result.dependencies: set[AnEntity] = dependencies

            # assign name
            if assign_name:
                if isinstance(result, Symbol):
                    result.name: str = name

                elif not hasattr(result, result._NAME_ATTR_KEY):
                    setattr(result, result._NAME_ATTR_KEY, name)

            return result

        if function.__name__ == _INIT_METHOD_NAME:
            self: AnEntity = args[0]
            assert isinstance(self, AnEntity)

            assert result is None

            # assign dependencies
            if not hasattr(self, self._DEPS_ATTR_KEY):
                self.dependencies: set[AnEntity] = dependencies - {self}

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

    setattr(func_w_deps_and_name_assignment, _ALREADY_DECORATED_ATTR_KEY, True)

    if not name_already_in_arg_spec:
        func_w_deps_and_name_assignment.__annotations__[_NAME_ATTR_KEY] = OptionalStrOrCallableReturningStr  # noqa: E501

        func_sig: Signature = signature(obj=function, follow_wrapped=False,
                                        globals=None, locals=None, eval_str=False)  # noqa: E501

        func_params: list[Any] = list(func_sig.parameters.values())

        name_param: Parameter = Parameter(name=_NAME_ATTR_KEY,
                                          kind=Parameter.KEYWORD_ONLY,
                                          default=default_name_factory,
                                          annotation=OptionalStrOrCallableReturningStr)  # noqa: E501

        try:
            kwargs_param_index: int = next(i
                                           for i, parameter in enumerate(func_params)  # noqa: E501
                                           if parameter.kind == Parameter.VAR_KEYWORD)  # noqa: E501

        except StopIteration:
            func_params.append(name_param)

        else:
            func_params.insert(kwargs_param_index, name_param)

        func_w_deps_and_name_assignment.__signature__: Signature = (
            func_sig.replace(parameters=func_params))

    if debug.ON:
        print(f'DECORATED {_func_qualname_and_signature(func_w_deps_and_name_assignment)}')  # noqa: E501
        pprint(describe(func_w_deps_and_name_assignment).__dict__,
               stream=None,
               indent=2,
               width=80,
               depth=None,
               compact=False,
               sort_dicts=False,
               underscore_numbers=False)

    return func_w_deps_and_name_assignment


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
        if isfunction(object=(__new__ := class_members.pop(_NEW_METHOD_NAME))):
            entity_related_callable.__new__: Callable[..., AnEntity] = \
                _decorate(__new__,
                          assign_name=(True
                                       if entity_related_callable._NAME_NULLABLE  # noqa: E501
                                       else UNIQUE_NAME_FACTORY))

            if debug.ON:
                print()

        # if __init__ is implemented somewhere in __mro__
        if isfunction(object=(__init__ := class_members.pop(_INIT_METHOD_NAME))):  # noqa: E501
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
                        print(f'DECORATING STATIC METHOD '
                              f'{_func_qualname_and_signature(class_member)}')
                        pprint(describe(class_member).__dict__,
                               stream=None,
                               indent=2,
                               width=80,
                               depth=None,
                               compact=False,
                               sort_dicts=False,
                               underscore_numbers=False)
                        print('==>')

                    setattr(entity_related_callable, class_member_name,
                            staticmethod(_decorate(class_member,
                                                   assign_name=True)))

                    if debug.ON:
                        decorated_class_member: Callable[..., AnEntity] = \
                            getattr(entity_related_callable, class_member_name)

                        print('==>')
                        print(f'DECORATED STATIC METHOD '
                              f'{_func_qualname_and_signature(decorated_class_member)}')  # noqa: E501
                        pprint(describe(decorated_class_member).__dict__,
                               stream=None,
                               indent=2,
                               width=80,
                               depth=None,
                               compact=False,
                               sort_dicts=False,
                               underscore_numbers=False)
                        print()

                # Unbound Instance Method
                else:
                    assert is_instance_method(class_member, bound=False)

                    if debug.ON:
                        print(f'DECORATING UNBOUND INSTANCE METHOD '
                              f'{_func_qualname_and_signature(class_member)}')
                        pprint(describe(class_member).__dict__,
                               stream=None,
                               indent=2,
                               width=80,
                               depth=None,
                               compact=False,
                               sort_dicts=False,
                               underscore_numbers=False)
                        print('==>')

                    setattr(entity_related_callable, class_member_name,
                            _decorate(class_member, assign_name=True))

                    if debug.ON:
                        decorated_class_member: Callable[..., AnEntity] = \
                            getattr(entity_related_callable, class_member_name)

                        print('==>')
                        print(f'DECORATED UNBOUND INSTANCE METHOD '
                              f'{_func_qualname_and_signature(decorated_class_member)}')  # noqa: E501
                        pprint(describe(decorated_class_member).__dict__,
                               stream=None,
                               indent=2,
                               width=80,
                               depth=None,
                               compact=False,
                               sort_dicts=False,
                               underscore_numbers=False)
                        print()

            # Class Method
            elif is_class_method(class_member) and _decorable(class_member.__func__):  # noqa: E501
                if debug.ON:
                    print(f'DECORATING CLASS METHOD '
                          f'{_func_qualname_and_signature(class_member)}')
                    pprint(describe(class_member).__dict__,
                           stream=None,
                           indent=2,
                           width=80,
                           depth=None,
                           compact=False,
                           sort_dicts=False,
                           underscore_numbers=False)
                    print('==>')

                setattr(entity_related_callable, class_member_name,
                        classmethod(_decorate(class_member.__func__,
                                              assign_name=True)))

                if debug.ON:
                    decorated_class_member: Callable[..., AnEntity] = \
                        getattr(entity_related_callable, class_member_name)

                    print('==>')
                    print(f'DECORATED CLASS METHOD '
                          f'{_func_qualname_and_signature(decorated_class_member)}')  # noqa: E501
                    pprint(describe(decorated_class_member).__dict__,
                           stream=None,
                           indent=2,
                           width=80,
                           depth=None,
                           compact=False,
                           sort_dicts=False,
                           underscore_numbers=False)
                    print()

            # Property's Underlying Getter Function
            elif is_property(class_member):
                if debug.ON:
                    print("DECORATING INSTANCE PROPERTY'S GETTER FUNCTION...")

                setattr(entity_related_callable, class_member_name,
                        property(fget=_decorate(class_member.fget,
                                                assign_name=False),
                                 fset=class_member.fset,
                                 fdel=class_member.fdel,
                                 doc=class_member.__doc__))

                if debug.ON:
                    print()

            # Cached Property's Underlying Function
            elif is_cached_property(class_member):
                if debug.ON:
                    print("DECORATING INSTANCE CACHED PROPERTY'S "
                          'UNDERLYING FUNCTION...')

                setattr(entity_related_callable, class_member_name,
                        cached_property(func=_decorate(class_member.func,
                                                       assign_name=False)))

                if debug.ON:
                    print()

        return entity_related_callable

    return _decorate(entity_related_callable, assign_name=True)
