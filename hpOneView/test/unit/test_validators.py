from unittest import TestCase

from hpOneView.validators import RequiredFields


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
