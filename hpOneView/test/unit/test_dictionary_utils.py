from unittest import TestCase

from hpOneView.dictionary_utils import get_dict_property, list_has_index


class DictionaryUtilsTest(TestCase):
    def setUp(self):
        self._list = ['a', 'b', 'c']
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
