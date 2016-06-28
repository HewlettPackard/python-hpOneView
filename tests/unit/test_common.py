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

from hpOneView import resource_compare


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

if __name__ == '__main__':
    unittest.main()
