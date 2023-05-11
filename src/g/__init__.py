"""Art of Geometry package."""


from collections.abc import Sequence
from importlib.metadata import version

from ._abc.session import Session
from ._util import debug


__all__: Sequence[str] = (
    '__version__',

    'Session',

    'debug',
)


__version__: str = version(distribution_name='Art-of-Geometry')
