__all__ = 'TMP_NAME_FACTORY', 'tmp_file_name', 'str_uuid'


import os
from tempfile import NamedTemporaryFile
from uuid import uuid4


def tmp_file_name():
    with NamedTemporaryFile() as named_tmp_file:
        return os.path.basename(named_tmp_file.name)


def str_uuid():
    return str(uuid4())


TMP_NAME_FACTORY = tmp_file_name
