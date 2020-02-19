__all__ = \
    'is_static_method', 'is_class_method', 'is_instance_method', 'is_instance_special_operator', \
    'describe'


from inspect import \
    getmembers, \
    isabstract, isclass, isfunction, ismethod, \
    isdatadescriptor, ismemberdescriptor, ismethoddescriptor, isgetsetdescriptor
from types import SimpleNamespace

from ._compat import cached_property


def is_static_method(obj) -> bool:
    return isfunction(obj) \
       and isfunction(getattr(obj, '__func__', None))


def is_class_method(obj) -> bool:
    return ismethod(obj) \
       and isclass(obj.__self__) \
       and isfunction(obj.__func__)


def is_instance_method(obj, /, *, bound: bool = True) -> bool:
    if bound:
        return ismethod(obj) \
           and (not isclass(obj.__self__))

    else:
        return isfunction(obj) \
           and (not hasattr(obj, '__self__'))


def is_instance_special_operator(obj, /, *, bound: bool = True) -> bool:
    return is_instance_method(obj, bound=bound) \
       and (name := obj.__name__).startswith('__') \
       and name.endswith('__')


def describe(obj, /, is_class: bool = False) -> SimpleNamespace:
    if is_class:
        return SimpleNamespace(
                **{class_member_name: describe(class_member)
                   for class_member_name, class_member in getmembers(obj)})

    else:
        descriptions = SimpleNamespace(Is=[])

        func = obj

        if isabstract(obj):
            descriptions.Is.append('Abstract')

        if isclass(obj):
            descriptions.Is.append('Class')

        if is_function := isfunction(obj):
            descriptions.Is.append('Function')

        if is_method := ismethod(obj):
            descriptions.Is.append('Method')

        if is_static_method(obj):
            descriptions.Is.append('StaticMethod')
            func = obj.__func__

        if is_class_method(obj):
            descriptions.Is.append('ClassMethod')
            func = obj.__func__

        if is_bound_instance_method := is_instance_method(obj, bound=True):
            descriptions.Is.append('InstanceMethodBound')
        elif is_unbound_instance_method := is_instance_method(obj, bound=False):
            descriptions.Is.append('InstanceMethodUnbound')

        if is_bound_instance_special_operator := is_instance_special_operator(obj, bound=True):
            descriptions.Is.append('InstanceSpecialOperatorBound')
        elif is_unbound_instance_special_operator := is_instance_special_operator(obj, bound=False):
            descriptions.Is.append('InstanceSpecialOperatorUnbound')

        if is_property := isinstance(obj, property):
            descriptions.Is.append('Property')
            func = obj.fget

        if is_cached_property := isinstance(obj, cached_property):
            descriptions.Is.append('CachedProperty')
            func = obj.func

        if isdatadescriptor(obj):
            descriptions.Is.append('DataDescriptor')

        if ismemberdescriptor(obj):
            descriptions.Is.append('MemberDescriptor')

        if ismethoddescriptor(obj):
            descriptions.Is.append('MethodDescriptor')

        if isgetsetdescriptor(obj):
            descriptions.Is.append('GetSetDescriptor')

        if is_function or is_method or \
                is_static_method or is_class_method or \
                is_bound_instance_method or is_unbound_instance_method or \
                is_bound_instance_special_operator or is_unbound_instance_special_operator or \
                is_property or is_cached_property:
            descriptions.Annotations = func.__annotations__

        return descriptions
