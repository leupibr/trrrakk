import functools
from os import path

from setuptools_scm import get_version


@functools.lru_cache()
def version_processor(request):
    try:
        return {'version': get_version(version_scheme='post-release')}
    except:
        return {'version': 'Release Notes'}

