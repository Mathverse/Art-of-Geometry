"""Inspect Class Object."""


from inspect import isclass


class C:
    """A Class."""


print(isclass(C))
