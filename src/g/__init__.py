"""Art of Geometry package."""


from collections.abc import Sequence
from importlib.metadata import version
from typing import LiteralString

from .session import Session
from .variable import Variable, Var
from ._util import debug


__all__: Sequence[LiteralString] = (
    '__version__',

    'Session',

    'Variable', 'Var',

    'debug',
)


__version__: LiteralString = version(distribution_name='Art-of-Geometry')
