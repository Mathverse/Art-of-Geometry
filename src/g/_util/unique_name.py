"""Unique Name Utilities."""


from collections.abc import Sequence
import os
from tempfile import NamedTemporaryFile
from uuid import uuid4

from .type import CallableReturningStr


__all__: Sequence[str] = 'UNIQUE_NAME_FACTORY', 'tmp_file_name', 'str_uuid'


def tmp_file_name() -> str:
    """Return temporary file name."""
    with NamedTemporaryFile(mode='w+b',
                            buffering=- 1,
                            encoding=None,
                            newline=None,
                            suffix=None,
                            prefix=None,
                            dir=None,
                            delete=True,
                            errors=None) as named_tmp_file:
        return os.path.basename(named_tmp_file.name)


def str_uuid() -> str:
    """Return string UUID."""
    return str(uuid4())


UNIQUE_NAME_FACTORY: CallableReturningStr = tmp_file_name
