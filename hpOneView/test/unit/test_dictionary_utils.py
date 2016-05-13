from unittest import TestCase

from hpOneView.dictionary_utils import get_dict_property


class DictionaryUtilsTest(TestCase):
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
