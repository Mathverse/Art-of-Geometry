"""Inspection Utilities."""


from __future__ import annotations

from functools import cached_property
from inspect import (getmembers,
                     isabstract,
                     isasyncgen, isasyncgenfunction,
                     isawaitable,
                     isbuiltin,
                     isclass,
                     iscode,
                     iscoroutine, iscoroutinefunction,
                     isdatadescriptor,
                     isframe,
                     isfunction,
                     isgenerator, isgeneratorfunction,
                     isgetsetdescriptor,
                     ismemberdescriptor,
                     ismethod,
                     ismethoddescriptor,
                     ismethodwrapper,
                     ismodule,
                     isroutine,
                     istraceback)
from types import SimpleNamespace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('is_static_method',
                                    'is_class_method',
                                    'is_instance_method',
                                    'is_instance_special_operator',
                                    'describe')


def is_static_method(obj, /) -> bool:
    """Check if object is static method."""
    return (isfunction(object=obj) and
            isclass(object=getattr(obj, '__class__', None)))


def is_class_method(obj, /) -> bool:
    """Check if object is class method."""
    return (ismethod(object=obj) and
            isclass(object=obj.__self__) and
            isfunction(object=obj.__func__))


def is_instance_method(obj, /, *, bound: bool = True) -> bool:
    """Check if object is instance method."""
    return ((ismethod(object=obj) and (not isclass(object=obj.__self__)))
            if bound
            else (isfunction(object=obj) and (not hasattr(obj, '__self__'))))


def is_instance_special_operator(obj, /, *, bound: bool = True) -> bool:
    """Check if object is instance special operator."""
    return (is_instance_method(obj, bound=bound) and
            (name := obj.__name__).startswith('__') and name.endswith('__'))


def is_property(obj, /) -> bool:
    """Check if object is property."""
    return (isinstance(obj, property) and callable(obj.fget))


def is_settable_property(obj, /) -> bool:
    """Check if object is settable property."""
    return (isinstance(obj, property) and callable(obj.fget) and callable(obj.fset))  # noqa: E501


def is_settable_deletable_property(obj, /) -> bool:
    """Check if object is settable & deletable property."""
    return (isinstance(obj, property) and callable(obj.fget) and
            callable(obj.fset) and callable(obj.fdel))


def is_cached_property(obj, /) -> bool:
    """Check if object is cached property."""
    return (isinstance(obj, cached_property) and callable(obj.func))


def describe(obj, /, is_class: bool = False) -> SimpleNamespace:  # noqa: C901,E501,PLR0915
    """Describe object."""
    if is_class:
        return SimpleNamespace(
            **{class_member_name: describe(class_member)
               for class_member_name, class_member in getmembers(obj)})

    descriptions: SimpleNamespace = SimpleNamespace(Is=[])

    func: Callable = obj

    if isabstract(object=obj):
        descriptions.Is.append('Abstract')

    if isclass(object=obj):
        descriptions.Is.append('Class')

    if is_function := isfunction(object=obj):
        descriptions.Is.append('Function')

    if is_method := ismethod(object=obj):
        descriptions.Is.append('Method')

    if is_static_method(obj):
        descriptions.Is.append('StaticMethod')
        func: Callable = obj

    if is_class_method(obj):
        descriptions.Is.append('ClassMethod')
        func: Callable = obj.__func__

    if is_bound_instance_method := is_instance_method(obj, bound=True):
        descriptions.Is.append('InstanceMethodBound')
    elif is_unbound_instance_method := is_instance_method(obj, bound=False):
        descriptions.Is.append('InstanceMethodUnbound')

    if (is_bound_instance_special_operator :=
            is_instance_special_operator(obj, bound=True)):
        descriptions.Is.append('InstanceSpecialOperatorBound')
    elif (is_unbound_instance_special_operator :=
            is_instance_special_operator(obj, bound=False)):
        descriptions.Is.append('InstanceSpecialOperatorUnbound')

    if _is_property := (is_property(obj) or
                        is_settable_property(obj) or
                        is_settable_deletable_property(obj)):
        descriptions.Is.append('Property')
        func: Callable = obj.fget

    if _is_cached_property := is_cached_property(obj):
        descriptions.Is.append('CachedProperty')
        func: Callable = obj.func

    if isdatadescriptor(object=obj):
        descriptions.Is.append('DataDescriptor')

    if ismethoddescriptor(object=obj):
        descriptions.Is.append('MethodDescriptor')

    # generators only
    if isgenerator(object=obj):
        descriptions.Is.append('Generator')

    if isgeneratorfunction(obj=obj):
        descriptions.Is.append('GeneratorFunction')

    # asynchronous implementations only
    if isasyncgen(object=obj):
        descriptions.Is.append('AsyncGen')

    if isasyncgenfunction(obj=obj):
        descriptions.Is.append('AsyncGenFunction')

    if isawaitable(object=obj):
        descriptions.Is.append('Awaitable')

    if iscoroutine(object=obj):
        descriptions.Is.append('Coroutine')

    if iscoroutinefunction(obj=obj):
        descriptions.Is.append('CoroutineFunction')

    # C implementations only
    if isgetsetdescriptor(object=obj):
        descriptions.Is.append('GetSetDescriptor')

    if ismemberdescriptor(object=obj):
        descriptions.Is.append('MemberDescriptor')

    # other, not relevant but just for completeness
    if isbuiltin(object=obj):
        descriptions.Is.append('BuiltIn')

    if iscode(object=obj):
        descriptions.Is.append('Code')

    if isframe(object=obj):
        descriptions.Is.append('Frame')

    if ismodule(object=obj):
        descriptions.Is.append('Module')

    if istraceback(object=obj):
        descriptions.Is.append('Traceback')

    if (is_function or is_method or
            is_static_method or is_class_method or
            is_bound_instance_method or is_unbound_instance_method or
            is_bound_instance_special_operator or
            is_unbound_instance_special_operator or
            _is_property or _is_cached_property):
        descriptions.Annotations = getattr(func, '__annotations__', None)

    return descriptions
