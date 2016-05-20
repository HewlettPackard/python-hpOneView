from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from future import standard_library

standard_library.install_aliases()


class RequiredFields:
    """Validate if all required properties are present on the dictionary that is passed to the class method.
    Only works for class methods and for the first method argument.

    E.g.:
    class FakeResource(object):
        @RequiredFields("source.name", "id")
        def method_test(self, dictionary_to_validate):
            pass
    """

    def __init__(self, *required_fields):
        self.__required_fields = required_fields
        self.__dictionary = None

    def __call__(self, function):

        def wrapper(*args, **kwargs):
            function_dict = self.__get_function_dict(args)
            missing = []
            for req in self.__required_fields:
                if not get_dict_property(function_dict, req):
                    missing.append(req)
            if missing:
                message = "Inform all required fields. Missing: " + (' '.join([str(i) + ';' for i in missing]))
                raise ValueError(message)

            function(*args, **kwargs)

        return wrapper

    def __none_argument(self):
        raise ValueError("Required fields can not be validated. Dictionary not found.")

    def __get_function_dict(self, args):

        try:
            _dict = args[1]
            if not _dict:
                self.__none_argument()

            if not isinstance(_dict, dict):
                raise ValueError("Validation requires a 'dict' argument , '%s' given" % _dict.__class__.__name__)
            return _dict
        except IndexError:
            self.__none_argument()


def get_dict_property(_dict, property):
    """ Find a property in the given dictionary
    E.g.:
    property:
        'A.B.data[0].info'
    dictionary:
        {
          "A": {
            "B": {
              "data": [
                {
                  "info": "TEXT"
                }
              ]
            }
          }
        }
    Args:
        _dict(dict):
            The dictionary
        property(str):
            The full name of the property.
    Returns:
        The value of the found property
    """

    keys = __get_property_dict_parts(property)
    for key, value in enumerate(keys):
        k = keys[key]
        if k in _dict:
            _dict = _dict[k]
        elif type(_dict) is list and list_has_index(_dict, k):
            list_key = int(k)
            _dict = _dict[list_key]
        else:
            return
    return _dict


def __get_property_dict_parts(property):
    property_to_format = re.sub("\[(\w+)\]", '.%s', property)
    substitutions = re.findall("\[(\w+)\]", property)
    parsed_property = property_to_format % tuple(substitutions)
    keys = parsed_property.split('.')
    return keys


def list_has_index(list, index):
    if int(index) < 0:
        index = abs(index + 1)
    return int(index) < len(list)
