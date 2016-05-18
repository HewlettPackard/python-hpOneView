import re


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
