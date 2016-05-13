from hpOneView.dictionary_utils import get_dict_property


class RequiredFields:
    """Validate if all required properties are present on the dictionary that is passed to the class method.
    Only works for class methods and for the first method argument.

    E.g.:
    class FakeResource(object):
        @RequiredFields("source.name", "id")
        def method_test(self, dictionary_to_validate):
            pass
    """

    def __init__(self, *requireds):
        self.__requireds = requireds

    def __call__(self, obj):
        def wrap(class_instance, dictionary):
            missing = []
            for req in self.__requireds:
                if not get_dict_property(dictionary, req):
                    missing.append(req)
            if missing:
                message = "Inform all required fileds. Missing: " + (' '.join([str(i) + ';' for i in missing]))
                raise ValueError(message)

        return wrap
