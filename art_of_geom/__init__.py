__all__ = ()


import os
from ruamel import yaml
from sys import version_info


_METADATA_FILE_NAME = 'metadata.yml'

_metadata = \
    yaml.safe_load(
        stream=open(os.path.join(
                        os.path.dirname(__file__),
                        _METADATA_FILE_NAME)))

_PKG_VER = '{} {}'.format(_metadata['PACKAGE'], _metadata['VERSION'])


# verify Python version
_MIN_PY_VER = 3, 8

assert version_info >= _MIN_PY_VER, \
   SystemError(f'*** {_PKG_VER} requires Python >= {_MIN_PY_VER} ***')
