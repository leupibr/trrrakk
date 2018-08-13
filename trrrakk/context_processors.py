import functools

from setuptools_scm import get_version


@functools.lru_cache()
def version_processor(request):
    return {'version': get_version(version_scheme='post-release')}
