__all__ = 'describe',


from inspect import \
    getmembers, \
    isabstract, isclass, isfunction, ismethod, \
    isdatadescriptor, ismemberdescriptor, ismethoddescriptor, isgetsetdescriptor


def describe(obj):
    return {class_member_name: describe(class_member)
            for class_member_name, class_member in getmembers(obj)} \
        if isclass(obj) \
      else dict(
            Abstract=isabstract(obj),
            Class=isclass(obj),
            Function=isfunction(obj),
            Method=ismethod(obj),
            DataDescriptor=isdatadescriptor(obj),
            MemberDescriptor=ismemberdescriptor(obj),
            MethodDescriptor=ismethoddescriptor(obj),
            GetSetDescriptor=isgetsetdescriptor(obj))
