from setuptools_scm import get_version


def version_processor(request):
    return {'version': get_version(version_scheme='post-release')}
