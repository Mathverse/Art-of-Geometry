"""Inspection Utilities."""


from __future__ import annotations

from functools import cached_property
from inspect import (getmembers,
                     isabstract, isclass, isfunction, ismethod,
                     isdatadescriptor,
                     ismemberdescriptor,
                     ismethoddescriptor,
                     isgetsetdescriptor)
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
            isfunction(object=getattr(obj, '__func__', None)))


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


def is_cached_property(obj, /) -> bool:
    """Check if object is cached property."""
    return (isinstance(obj, cached_property) and callable(obj.func))


def describe(obj, /, is_class: bool = False) -> SimpleNamespace:  # noqa: C901
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
        func: Callable = obj.__func__

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

    if _is_property := is_property(obj):
        descriptions.Is.append('Property')
        func: Callable = obj.fget

    if _is_cached_property := is_cached_property(obj):
        descriptions.Is.append('CachedProperty')
        func: Callable = obj.func

    if isdatadescriptor(object=obj):
        descriptions.Is.append('DataDescriptor')

    if ismemberdescriptor(object=obj):
        descriptions.Is.append('MemberDescriptor')

    if ismethoddescriptor(object=obj):
        descriptions.Is.append('MethodDescriptor')

    if isgetsetdescriptor(object=obj):
        descriptions.Is.append('GetSetDescriptor')

    if (is_function or is_method or
            is_static_method or is_class_method or
            is_bound_instance_method or is_unbound_instance_method or
            is_bound_instance_special_operator or
            is_unbound_instance_special_operator or
            _is_property or _is_cached_property):
        descriptions.Annotations = getattr(func, '__annotations__', None)

    return descriptions
