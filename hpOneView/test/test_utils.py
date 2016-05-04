import sys


def mock_builtin(method_name='open'):
    package_name = 'builtins' if sys.version_info[:3] >= (3,) else '__builtin__'
    return "%s.%s" % (package_name, method_name)
