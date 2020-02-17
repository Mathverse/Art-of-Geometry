__all__ = 'cached_property',


from sys import version_info

from .. import _MIN_PY_VER


if version_info >= _MIN_PY_VER:
    from functools import cached_property

else:
    from cached_property import cached_property
