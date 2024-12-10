"""Inspect Class Object."""


from inspect import isclass


class C:
    """A Class."""


print(f'{C} Is Class? {isclass(C)}')
