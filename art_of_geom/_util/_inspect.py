__all__ = 'describe',


from inspect import \
    getmembers, \
    isabstract, isclass, isfunction, ismethod, \
    isdatadescriptor, ismemberdescriptor, ismethoddescriptor, isgetsetdescriptor


def describe(obj, /, Class=False):
    return {class_member_name: describe(class_member)
            for class_member_name, class_member in getmembers(obj)} \
        if Class \
      else dict(
            Abstract=isabstract(obj),
            Class=isclass(obj),
            Function=(is_function := isfunction(obj)),
            Method=(is_method := ismethod(obj)),
            Annotations=
                obj.__annotations__
                if is_function or is_method
                else None,
            DataDescriptor=isdatadescriptor(obj),
            MemberDescriptor=ismemberdescriptor(obj),
            MethodDescriptor=ismethoddescriptor(obj),
            GetSetDescriptor=isgetsetdescriptor(obj))
