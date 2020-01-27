import os
from ruamel import yaml
from setuptools import find_packages, setup


_PACKAGE_NAMESPACE_NAME = 'art_of_geom'

_METADATA_FILE_NAME = 'metadata.yml'

_SETUP_REQUIREMENTS_FILE_NAME = 'requirements-setup.txt'
_CORE_REQUIREMENTS_FILE_NAME = 'requirements-core.txt'
_DOC_REQUIREMENTS_FILE_NAME = 'requirements-doc.txt'
_JUPYTER_REQUIREMENTS_FILE_NAME = 'requirements-jupyter.txt'
_VIZ_REQUIREMENTS_FILE_NAME = 'requirements-viz.txt'


_metadata = \
    yaml.safe_load(
        stream=open(os.path.join(
                os.path.dirname(__file__),
                _PACKAGE_NAMESPACE_NAME,
                _METADATA_FILE_NAME)))


setup(
    name=_metadata['PACKAGE'],
    author=_metadata['AUTHOR'],
    author_email=_metadata['AUTHOR_EMAIL'],
    url=_metadata['URL'],
    version=_metadata['VERSION'],
    description=_metadata['DESCRIPTION'],
    long_description=_metadata['DESCRIPTION'],
    keywords=_metadata['DESCRIPTION'],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=
        [s for s in
            {i.strip()
             for i in open(_SETUP_REQUIREMENTS_FILE_NAME).readlines()}
         if not s.startswith('#')],
    install_requires=
        [s for s in
            {i.strip()
             for i in (open(_CORE_REQUIREMENTS_FILE_NAME).readlines() +
                       open(_DOC_REQUIREMENTS_FILE_NAME).readlines() +
                       open(_JUPYTER_REQUIREMENTS_FILE_NAME).readlines() +
                       open(_VIZ_REQUIREMENTS_FILE_NAME).readlines())}
         if not s.startswith('#')])
