# -*- coding: utf-8 -*-
###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
import unittest

from hpOneView import resource_compare, transform_list_to_dict, extract_id_from_uri, merge_list_by_key


class ResourceCompareTest(unittest.TestCase):
    DICT_ORIGINAL = {u'status': u'OK', u'category': u'fcoe-networks',
                     u'description': None, u'created': u'2016-06-13T20:39:15.991Z',
                     u'uri': u'/rest/fcoe-networks/36c56106-3b14-4f0d-8df9-627700b8e01b',
                     u'state': u'Active',
                     u'vlanId': 201,
                     u'modified': u'2016-06-13T20:39:15.993Z',
                     u'fabricUri': u'/rest/fabrics/a3cff65e-6d95-4d4d-9047-3548b6aca902',
                     u'eTag': u'7275bfe5-2e41-426a-844a-9eb00ac8be41', u'managedSanUri': None,
                     u'connectionTemplateUri': u'/rest/connection-templates/0799d26c-68db-4b4c-b007-d31cf9d60a2f',
                     u'type': u'fcoe-network',
                     u"sub": {
                         "ssub": "ssub",
                         'fs_item': 1,
                         'level3': {
                             "lvl3_t1": "lvl3_t1"
                         },
                         "list": [1, 2, "3"]
                     },
                     u'name': u'Test FCoE Network'}

    DICT_EQUAL_ORIGINAL = {u'status': u'OK', u'category': u'fcoe-networks',
                           u'description': None, u'created': u'2016-06-13T20:39:15.991Z',
                           u'uri': u'/rest/fcoe-networks/36c56106-3b14-4f0d-8df9-627700b8e01b',
                           u'vlanId': '201',
                           "sub": {
                               "ssub": "ssub",
                               'fs_item': "1",
                               'level3': {
                                   "lvl3_t1": u"lvl3_t1"
                               },
                               "list": [1, 2, '3']
                           },
                           u'modified': u'2016-06-13T20:39:15.993Z',
                           u'fabricUri': u'/rest/fabrics/a3cff65e-6d95-4d4d-9047-3548b6aca902',
                           u'state': u'Active',
                           u'eTag': u'7275bfe5-2e41-426a-844a-9eb00ac8be41', u'managedSanUri': None,
                           u'connectionTemplateUri': u'/rest/connection-templates/0799d26c-68db-4b4c-b007-d31cf9d60a2f',
                           u'type': u'fcoe-network',
                           u'name': 'Test FCoE Network'}

    DICT_DIF_ORIGINAL_LV3 = {u'status': u'OK', u'category': u'fcoe-networks',
                             u'description': None, u'created': u'2016-06-13T20:39:15.991Z',
                             u'uri': u'/rest/fcoe-networks/36c56106-3b14-4f0d-8df9-627700b8e01b',
                             u'vlanId': '201',
                             "sub": {
                                 "ssub": "ssub",
                                 'fs_item': "1",
                                 'level3': {
                                     "lvl3_t1": u"lvl3_t1x"
                                 },
                                 "list": [1, 2, 3]
                             },
                             u'modified': u'2016-06-13T20:39:15.993Z',
                             u'fabricUri': u'/rest/fabrics/a3cff65e-6d95-4d4d-9047-3548b6aca902',
                             u'state': u'Active',
                             u'eTag': u'7275bfe5-2e41-426a-844a-9eb00ac8be41', u'managedSanUri': None,
                             u'connectionTemplateUri':
                                 u'/rest/connection-templates/0799d26c-68db-4b4c-b007-d31cf9d60a2f',
                             u'type': u'fcoe-network',
                             u'name': 'Test FCoE Network'}

    DICT_EMPTY_NONE1 = {
        "name": "Enclosure Group 1",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                },
                {
                    "interconnectBay": 2,
                },
            ]
    }

    DICT_EMPTY_NONE2 = {
        "name": "Enclosure Group 1",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                    'logicalInterconnectGroupUri': None
                },
                {
                    "interconnectBay": 2,
                    'logicalInterconnectGroupUri': None
                },
            ]
    }

    DICT_EMPTY_NONE3 = {
        "name": "Enclosure Group 1",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                    'logicalInterconnectGroupUri': ''
                },
                {
                    "interconnectBay": 2,
                    'logicalInterconnectGroupUri': None
                },
            ]
    }

    def test_resource_compare_equals(self):
        self.assertTrue(resource_compare(self.DICT_ORIGINAL, self.DICT_EQUAL_ORIGINAL))

    def test_resource_compare_missing_entry_in_first(self):
        dict1 = self.DICT_ORIGINAL.copy()
        del dict1['state']

        self.assertFalse(resource_compare(dict1, self.DICT_EQUAL_ORIGINAL))

    def test_resource_compare_missing_entry_in_second(self):
        dict2 = self.DICT_EQUAL_ORIGINAL.copy()
        del dict2['state']

        self.assertFalse(resource_compare(self.DICT_ORIGINAL, self.DICT_DIF_ORIGINAL_LV3))

    def test_resource_compare_different_on_level3(self):
        self.assertFalse(resource_compare(self.DICT_ORIGINAL, self.DICT_DIF_ORIGINAL_LV3))

    def test_resource_compare_equals_with_empty_eq_none(self):
        self.assertTrue(resource_compare(self.DICT_EMPTY_NONE1, self.DICT_EMPTY_NONE2))

    def test_resource_compare_equals_with_empty_eq_none_inverse(self):
        self.assertTrue(resource_compare(self.DICT_EMPTY_NONE2, self.DICT_EMPTY_NONE1))

    def test_resource_compare_equals_with_empty_eq_none_different(self):
        self.assertFalse(resource_compare(self.DICT_EMPTY_NONE3, self.DICT_EMPTY_NONE1))

    def test_resource_compare_with_double_level_list(self):
        dict1 = {list: [
            [1, 2, 3],
            [4, 5, 6]
        ]}

        dict2 = {list: [
            [1, 2, 3],
            [4, 5, "6"]
        ]}

        self.assertTrue(resource_compare(dict1, dict2))

    def test_resource_compare_with_double_level_list_different(self):
        dict1 = {list: [
            [1, 2, 3],
            [4, 5, 6]
        ]}

        dict2 = {list: [
            [1, 2, 3],
            [4, 5, "7"]
        ]}

        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_with_int_and_float(self):
        dict1 = {
            "name": "name",
            "lvalue": int(10)
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10)
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_with_str_and_integer_float(self):
        dict1 = {
            "name": "name",
            "lvalue": '10'
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10)
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_with_str_and_float(self):
        dict1 = {
            "name": "name",
            "lvalue": '10.1'
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10.1)
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_dict_and_list(self):
        dict1 = {
            "name": "name",
            "value": {"id": 123}
        }

        dict2 = {
            "name": "name",
            "value": [1, 2, 3]
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_list_and_dict(self):
        dict1 = {
            "name": "name",
            "value": [1, 2, 3]
        }

        dict2 = {
            "name": "name",
            "value": {"id": 123}
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_with_different_float_values(self):
        dict1 = {
            "name": "name",
            "lvalue": 10.2
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10.1)
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_empty_list_and_none(self):
        dict1 = {
            "name": "name",
            "values": []
        }

        dict2 = {
            "name": "name",
            "values": None
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_none_and_empty_list(self):
        dict1 = {
            "name": "name",
            "values": None
        }
        dict2 = {
            "name": "name",
            "values": []
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_true_and_false(self):
        dict1 = {
            "name": "name",
            "values": True
        }

        dict2 = {
            "name": "name",
            "values": False
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_false_and_true(self):
        dict1 = {
            "name": "name",
            "values": False
        }

        dict2 = {
            "name": "name",
            "values": True
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_true_and_true(self):
        dict1 = {
            "name": "name",
            "values": True
        }

        dict2 = {
            "name": "name",
            "values": True
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_false_and_false(self):
        dict1 = {
            "name": "name",
            "values": False
        }

        dict2 = {
            "name": "name",
            "values": False
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_none_and_false(self):
        dict1 = {
            "name": "name",
            "values": None
        }

        dict2 = {
            "name": "name",
            "values": False
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_false_and_none(self):
        dict1 = {
            "name": "name",
            "values": False
        }
        dict2 = {
            "name": "name",
            "values": None
        }
        self.assertTrue(resource_compare(dict1, dict2))

    def test_comparison_list_and_none_level_1(self):
        dict1 = {
            "name": "name of the resource",
            "value": [{"name": "item1"},
                      {"name": "item2"}]
        }
        dict2 = {
            "name": "name of the resource",
            "value": None
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_none_and_list_level_1(self):
        dict1 = {
            "name": "name",
            "value": None
        }
        dict2 = {
            "name": "name",
            "value": [{"name": "item1"},
                      {"name": "item2"}]
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_dict_and_none_level_1(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource"}
        }
        dict2 = {
            "name": "name",
            "value": None
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_none_and_dict_level_1(self):
        dict1 = {
            "name": "name",
            "value": None
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource"}
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_none_and_dict_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": None}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": {
                          "name": "sub-sub-resource"
                      }}
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_dict_and_none_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": {
                          "name": "sub-sub-resource"
                      }}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": None}
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_none_and_list_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": None}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": ["item1", "item2"]}
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_comparison_list_and_none_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": ["item1", "item2"]}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": None}
        }
        self.assertFalse(resource_compare(dict1, dict2))

    def test_transform_list_to_dict(self):
        list = ['one', 'two', {'tree': 3}, 'four', 5]

        dict_transformed = transform_list_to_dict(list=list)

        self.assertEqual(dict_transformed,
                         {'5': True,
                          'four': True,
                          'one': True,
                          'tree': 3,
                          'two': True})

    def test_extract_id_from_uri(self):
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155'
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(id, extracted_id)

    def test_extract_id_from_uri_with_extra_slash(self):
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155/'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(extracted_id, '')

    def test_extract_id_from_uri_passing_id(self):
        uri = '3518be0e-17c1-4189-8f81-83f3724f6155'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(extracted_id, '3518be0e-17c1-4189-8f81-83f3724f6155')

    def test_extract_id_from_uri_unsupported(self):
        # This example is not supported yet
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155/otherthing'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(extracted_id, 'otherthing')

    def test_merge_list_by_key_when_original_list_is_empty(self):
        original_list = []
        list_with_changes = [dict(id=1, value="123")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, value="123")]
        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_when_original_list_is_null(self):
        original_list = None
        list_with_changes = [dict(id=1, value="123")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, value="123")]
        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_same_lenght_and_order(self):
        original_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1005)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_different_order(self):
        original_list = [dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000),
                         dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1005)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_removed_items(self):
        original_list = [dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000),
                         dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_added_items(self):
        original_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, requestedMbps=1005)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_should_ignore_key_when_null(self):
        original_list = [dict(id=1, value1="123", value2="345")]
        list_with_changes = [dict(id=1, value1=None, value2="345-changed")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id",
                                        ignore_when_null=['value1', 'value2'])

        expected_list = [dict(id=1, value1="123", value2="345-changed")]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_should_not_fail_when_ignored_key_absent(self):
        original_list = [dict(id=1, value1="123", value2="345")]
        list_with_changes = [dict(id=1, value3="678")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id",
                                        ignore_when_null=['value1'])

        expected_list = [dict(id=1, value1="123", value2="345", value3="678")]

        self.assertEqual(merged_list, expected_list)


if __name__ == '__main__':
    unittest.main()
