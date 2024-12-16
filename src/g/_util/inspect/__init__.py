"""Inspection Utilities."""


# docs.python.org/dev/library/inspect


from __future__ import annotations

from functools import cached_property
from inspect import (get_annotations, getmembers,
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
                     # ispackage,  # Python 3.14+
                     isroutine,
                     istraceback,
                     signature)
from types import SimpleNamespace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from inspect import Signature
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('is_static_method',
                                    'is_class_method',
                                    'is_instance_method',
                                    'is_instance_special_operator',
                                    'describe')


def is_static_method(obj, /) -> bool:
    """Check if object is static method."""
    if not (isfunction(object=obj) and ('.' in obj.__qualname__)):
        return False

    # relying on self-argument naming convention
    return 'self' not in signature(obj=obj, follow_wrapped=True,
                                   globals=None, locals=None, eval_str=True).parameters  # noqa: E501


def is_class_method(obj, /) -> bool:
    """Check if object is class method."""
    return (ismethod(object=obj) and
            isclass(object=obj.__self__) and
            isfunction(object=obj.__func__))


def is_instance_method(obj, /, *, bound: bool = True) -> bool:
    """Check if object is instance method."""
    if bound:
        return ismethod(object=obj) and (not isclass(object=obj.__self__))

    if not (isfunction(object=obj) and ('.' in obj.__qualname__)):
        return False

    # relying on self-argument naming convention
    return 'self' in signature(obj=obj, follow_wrapped=True,
                               globals=None, locals=None, eval_str=True).parameters  # noqa: E501


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
        return SimpleNamespace(**{class_member_name: describe(class_member)
                                  for class_member_name, class_member in
                                  getmembers(object=obj, predicate=None)})

    descriptions: SimpleNamespace = SimpleNamespace(Is=set())

    func: Callable = obj

    # Package & Module
    # ----------------
    # docs.python.org/dev/library/inspect.html#inspect.ispackage
    # if ispackage(object=obj):
    #     descriptions.Is.add('Package')

    # docs.python.org/dev/library/inspect.html#inspect.ismodule
    if ismodule(object=obj):
        descriptions.Is.add('Module')

    # Class
    # -----
    # docs.python.org/dev/library/inspect.html#inspect.isabstract
    if isabstract(object=obj):
        descriptions.Is.add('Abstract')

    # docs.python.org/dev/library/inspect.html#inspect.isclass
    if isclass(object=obj):
        descriptions.Is.add('Class')

    # Routine / Function / Method
    # ---------------------------
    # docs.python.org/dev/library/inspect.html#inspect.isroutine
    if _is_routine := isroutine(object=obj):
        descriptions.Is.add('Routine')

    # docs.python.org/dev/library/inspect.html#inspect.isfunction
    if _is_function := isfunction(object=obj):
        descriptions.Is.add('Function')

    # docs.python.org/dev/library/inspect.html#inspect.ismethod
    if _is_method := ismethod(object=obj):
        descriptions.Is.add('Method')

    if _is_static_method := is_static_method(obj):
        descriptions.Is.add('StaticMethod')
        func: Callable = obj

    if _is_class_method := is_class_method(obj):
        descriptions.Is.add('ClassMethod')
        func: Callable = obj.__func__

    if _is_bound_instance_method := is_instance_method(obj, bound=True):
        descriptions.Is.add('InstanceMethodBound')
    elif _is_unbound_instance_method := is_instance_method(obj, bound=False):
        descriptions.Is.add('InstanceMethodUnbound')

    if (_is_bound_instance_special_operator :=
            is_instance_special_operator(obj, bound=True)):
        descriptions.Is.add('InstanceSpecialOperatorBound')
    elif (_is_unbound_instance_special_operator :=
            is_instance_special_operator(obj, bound=False)):
        descriptions.Is.add('InstanceSpecialOperatorUnbound')

    # Data Descriptor / (Cached) Property
    # -----------------------------------
    # docs.python.org/dev/library/inspect.html#inspect.isdatadescriptor
    if isdatadescriptor(object=obj):
        descriptions.Is.add('DataDescriptor')

    if _is_property := (is_property(obj) or
                        is_settable_property(obj) or
                        is_settable_deletable_property(obj)):
        descriptions.Is.add('Property')
        func: Callable = obj.fget

    if _is_cached_property := is_cached_property(obj):
        descriptions.Is.add('CachedProperty')
        func: Callable = obj.func

    # for info only: Method Descriptor/Wrapper
    # ----------------------------------------
    # docs.python.org/dev/library/inspect.html#inspect.ismethoddescriptor
    if ismethoddescriptor(object=obj):
        descriptions.Is.add('MethodDescriptor')

    # docs.python.org/dev/library/inspect.html#inspect.ismethodwrapper
    if ismethodwrapper(object=obj):
        descriptions.Is.add('MethodWrapper')

    # for info only: Generator (Function)
    # -----------------------------------
    # docs.python.org/dev/library/inspect.html#inspect.isgenerator
    if isgenerator(object=obj):
        descriptions.Is.add('Generator')

    # docs.python.org/dev/library/inspect.html#inspect.isgeneratorfunction
    if isgeneratorfunction(obj=obj):
        descriptions.Is.add('GeneratorFunction')

    # for info only: Async-related
    # ----------------------------
    # docs.python.org/dev/library/inspect.html#inspect.isasyncgen
    if isasyncgen(object=obj):
        descriptions.Is.add('AsyncGen')

    # docs.python.org/dev/library/inspect.html#inspect.isasyncgenfunction
    if isasyncgenfunction(obj=obj):
        descriptions.Is.add('AsyncGenFunction')

    # docs.python.org/dev/library/inspect.html#inspect.isawaitable
    if isawaitable(object=obj):
        descriptions.Is.add('Awaitable')

    # docs.python.org/dev/library/inspect.html#inspect.iscoroutine
    if iscoroutine(object=obj):
        descriptions.Is.add('Coroutine')

    # docs.python.org/dev/library/inspect.html#inspect.iscoroutinefunction
    if iscoroutinefunction(obj=obj):
        descriptions.Is.add('CoroutineFunction')

    # for info only: C-implemented data descriptors
    # ---------------------------------------------
    # docs.python.org/dev/library/inspect.html#inspect.isgetsetdescriptor
    if isgetsetdescriptor(object=obj):
        descriptions.Is.add('GetSetDescriptor')

    # docs.python.org/dev/library/inspect.html#inspect.ismemberdescriptor
    if ismemberdescriptor(object=obj):
        descriptions.Is.add('MemberDescriptor')

    # for info only: other, not relevant but just for completeness
    # ------------------------------------------------------------
    # docs.python.org/dev/library/inspect.html#inspect.isbuiltin
    if isbuiltin(object=obj):
        descriptions.Is.add('BuiltIn')

    # docs.python.org/dev/library/inspect.html#inspect.iscode
    if iscode(object=obj):
        descriptions.Is.add('Code')

    # docs.python.org/dev/library/inspect.html#inspect.isframe
    if isframe(object=obj):
        descriptions.Is.add('Frame')

    # docs.python.org/dev/library/inspect.html#inspect.istraceback
    if istraceback(object=obj):
        descriptions.Is.add('Traceback')

    if (_is_routine or _is_function or _is_method or
            _is_static_method or _is_class_method or
            _is_bound_instance_method or _is_unbound_instance_method or
            _is_bound_instance_special_operator or
            _is_unbound_instance_special_operator or
            _is_property or _is_cached_property):
        descriptions.Signature: Signature = \
            signature(func, follow_wrapped=True,
                      globals=None, locals=None, eval_str=True)

        descriptions.Annotations: dict[str, type] = \
            get_annotations(func,
                            globals=None, locals=None, eval_str=True)

    return descriptions
