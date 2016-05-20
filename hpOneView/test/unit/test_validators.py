from unittest import TestCase

from hpOneView.validators import RequiredFields, list_has_index, get_dict_property


class FakeResource(object):
    @RequiredFields("source.name", "id")
    def method_test(self, dictionary):
        pass


class DictionaryValidatorTest(TestCase):
    def setUp(self):
        self.fakeResource = FakeResource()

    def test_should_not_raise_exception_when_all_requireds_are_present(self):
        dictionary = {
            "source": {
                "name": "Test"
            },
            "id": 1
        }

        self.fakeResource.method_test(dictionary)

    def test_should_raise_exception_when_required_fields_are_not_present(self):
        dictionary = {
            "index": "value"
        }
        expected_error_message = 'Inform all required fields. Missing: source.name; id;'
        try:
            self.fakeResource.method_test(dictionary)
        except ValueError as e:
            self.assertEqual(expected_error_message, e.args[0])
        else:
            self.fail('Exception not raised')

    def test_should_raise_exception_when_dict_not_pass_through_function(self):
        dictionary = None
        expected_error_message = 'Required fields can not be validated. Dictionary not found.'
        try:
            self.fakeResource.method_test(dictionary)
        except ValueError as e:
            self.assertEqual(expected_error_message, e.args[0])
        else:
            self.fail('Exception not raised')

    def test_should_raise_exception_when_argument_is_not_a_dict(self):
        dictionary = "false dictionary"
        expected_error_message = "Validation requires a 'dict' argument , 'str' given"
        try:
            self.fakeResource.method_test(dictionary)
        except ValueError as e:
            self.assertEqual(expected_error_message, e.args[0])
        else:
            self.fail('Exception not raised')


class GetDictPropertyTest(TestCase):
    def setUp(self):
        self.dictionary = {
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

    def test_should_return_the_property_value(self):
        property = 'A.B.data[0].info'

        result = get_dict_property(self.dictionary, property)
        self.assertEqual("TEXT", result)

    def test_return_none_when_property_not_exists(self):
        property = 'A.B.data[0].description'
        result = get_dict_property(self.dictionary, property)
        self.assertIsNone(result)


class ListHasIndexTest(TestCase):
    def setUp(self):
        self._list = ['a', 'b', 'c']

    def test_get_negative_list_index(self):
        _index = -3
        result = list_has_index(self._list, _index)
        self.assertTrue(result)

    def test_should_return_false_when_index_not_exists(self):
        _index = 3
        result = list_has_index(self._list, _index)
        self.assertFalse(result)

    def test_should_return_true_when_index_zero_exists(self):
        _index = 0
        result = list_has_index(self._list, _index)
        self.assertTrue(result)

    def test_should_return_false_when_index_zero_not_exists(self):
        _list = []
        _index = 0
        result = list_has_index(_list, _index)
        self.assertFalse(result)
