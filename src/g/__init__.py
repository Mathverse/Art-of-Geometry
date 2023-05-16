"""Art of Geometry package."""


from collections.abc import Sequence
from importlib.metadata import version
from typing import LiteralString

from .session import Session
from ._util import debug


__all__: Sequence[LiteralString] = (
    '__version__',

    'Session',

    'debug',
)


__version__: LiteralString = version(distribution_name='Art-of-Geometry')
