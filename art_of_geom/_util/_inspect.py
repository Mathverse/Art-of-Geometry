__all__ = \
    'is_class_method', 'is_special_op', \
    'describe'


from inspect import \
    getmembers, \
    isabstract, isclass, isfunction, ismethod, \
    isdatadescriptor, ismemberdescriptor, ismethoddescriptor, isgetsetdescriptor

from ._compat import cached_property


def is_class_method(obj) -> bool:
    return ismethod(obj) \
       and isclass(obj.__self__)


def is_special_op(obj) -> bool:
    return isfunction(obj) \
       and (name := obj.__name__).startswith('__') \
       and name.endswith('__')


def describe(obj, /, Class=False) -> dict:
    return {class_member_name: describe(class_member)
            for class_member_name, class_member in getmembers(obj)} \
        if Class \
      else dict(
            Abstract=isabstract(obj),
            Class=isclass(obj),
            Function=(is_function := isfunction(obj)),
            Method=(is_method := ismethod(obj)),
            SpecialOp=is_special_op(obj),
            Annotations=
                obj.__annotations__
                if is_function or is_method
                else None,
            DataDescriptor=isdatadescriptor(obj),
            MemberDescriptor=ismemberdescriptor(obj),
            MethodDescriptor=ismethoddescriptor(obj),
            GetSetDescriptor=isgetsetdescriptor(obj),
            ClassMethod=
                obj.__func__
                if is_class_method(obj)
                else False,
            Property=
                obj.fget
                if isinstance(obj, property)
                else False,
            CachedProperty=
                obj.func
                if isinstance(obj, cached_property)
                else False)
