__all__ = \
    'cached_property'


import os
from ruamel import yaml
from sys import version_info


_METADATA_FILE_NAME = 'metadata.yml'

_metadata = \
    yaml.safe_load(
        stream=open(os.path.join(
                        os.path.dirname(
                            os.path.dirname(
                                os.path.abspath(__file__))),
                        _METADATA_FILE_NAME)))

_PKG_VER = '{} {}'.format(_metadata['PACKAGE'], _metadata['VERSION'])


# verify Python version
_MIN_PY_VER = 3, 7

assert version_info >= _MIN_PY_VER, \
    '*** Arimo SDK {} requires Python >= {}.{} ***'.format(
        _PKG_VER, _MIN_PY_VER[0], _MIN_PY_VER[1])


PY38 = version_info >= (3, 8)


if PY38:
    from functools import cached_property

else:
    from cached_property import cached_property
