__all__ = 'cached_property',


from sys import version_info


if version_info >= (3, 8):
    from functools import cached_property

else:
    from cached_property import cached_property
