import hpOneView
import json
import os
import sys

ROOT_MODULE_DIR = os.path.dirname(hpOneView.__file__)


def load_stub(file_name):
    file = os.path.join(ROOT_MODULE_DIR, 'test', 'stubs', file_name)
    with open(file) as json_data:
        return json.load(json_data)

def mock_builtin(method_name='open'):
    package_name = 'builtins' if sys.version_info[:3] >= (3,) else '__builtin__'
    return "%s.%s" % (package_name, method_name)

