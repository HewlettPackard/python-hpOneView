# -*- coding: utf-8 -*-
###
# (C) Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from hpOneView.extras.comparators import resource_compare


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
                               "list": [1, '3', 2]
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

    def test_comparison_list_of_dicts_with_diff_order(self):
        resource1 = {'connections': [
            {
                u'allocatedMbps': 0,
                u'networkUri': u'/rest/fc-networks/617a2c3b-1505-4369-a0a5-4c169183bf9d',
                u'requestedMbps': u'2500',
                u'portId': u'None',
                u'name': u'connection2',
                u'maximumMbps': 0,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Reserved',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': u'10:00:c2:54:96:f0:00:03',
                u'mac': u'46:E0:32:50:00:01',
                u'macType': u'Virtual',
                u'wwpn': u'10:00:c2:54:96:f0:00:02',
                u'interconnectUri': None,
                u'requestedVFs': None,
                u'functionType': u'FibreChannel',
                u'id': 2,
                u'allocatedVFs': None
            },
            {
                u'allocatedMbps': 1000,
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'requestedMbps': u'1000',
                u'portId': u'Flb 1:1-a',
                u'name': u'connection3',
                u'maximumMbps': 1000,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Deployed',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': None,
                u'mac': u'46:E0:32:50:00:02',
                u'macType': u'Virtual',
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': u'Auto',
                u'functionType': u'Ethernet',
                u'id': 3,
                u'allocatedVFs': None
            },
            {
                u'allocatedMbps': 1000,
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'requestedMbps': u'1000',
                u'portId': u'Flb 1:2-a',
                u'name': u'connection4',
                u'maximumMbps': 1000,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Deployed',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': None,
                u'mac': u'46:E0:32:50:00:03',
                u'macType': u'Virtual',
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/a3c936f2-2993-4779-a6e3-dc302b6f1bc6',
                u'requestedVFs': u'Auto',
                u'functionType': u'Ethernet',
                u'id': 4,
                u'allocatedVFs': None
            },
            {
                u'allocatedMbps': 2500,
                u'networkUri': u'/rest/fc-networks/179222e0-d59e-4898-b2bf-5c053c872ee6',
                u'requestedMbps': u'2500',
                u'portId': u'Flb 1:1-b',
                u'name': u'connection1',
                u'maximumMbps': 10000,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Deployed',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': u'10:00:c2:54:96:f0:00:01',
                u'mac': u'46:E0:32:50:00:00',
                u'macType': u'Virtual',
                u'wwpn': u'10:00:c2:54:96:f0:00:00',
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': None,
                u'functionType': u'FibreChannel',
                u'id': 1,
                u'allocatedVFs': None
            }
        ]
        }

        resource2 = {'connections': [
            {
                u'requestedMbps': 1000,
                u'deploymentStatus': u'Deployed',
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'mac': u'46:E0:32:50:00:02',
                u'wwpnType': u'Virtual',
                u'id': 3,
                u'macType': u'Virtual',
                u'allocatedMbps': 1000,
                u'wwnn': None,
                u'maximumMbps': 1000,
                u'portId': u'Flb 1:1-a',
                u'name': 'connection3',
                u'functionType': 'Ethernet',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': u'Auto'
            },
            {
                u'requestedMbps': 1000,
                u'deploymentStatus': u'Deployed',
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'mac': u'46:E0:32:50:00:03',
                u'wwpnType': u'Virtual',
                u'id': 4,
                u'macType': u'Virtual',
                u'allocatedMbps': 1000,
                u'wwnn': None,
                u'maximumMbps': 1000,
                u'portId': u'Flb 1:2-a',
                u'name': 'connection4',
                u'functionType': 'Ethernet',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/a3c936f2-2993-4779-a6e3-dc302b6f1bc6',
                u'requestedVFs': u'Auto'
            },
            {
                u'requestedMbps': 2500,
                u'deploymentStatus': u'Deployed',
                u'networkUri': u'/rest/fc-networks/179222e0-d59e-4898-b2bf-5c053c872ee6',
                u'mac': u'46:E0:32:50:00:00',
                u'wwpnType': u'Virtual',
                u'id': 1,
                u'macType': u'Virtual',
                u'allocatedMbps': 2500,
                u'wwnn': u'10:00:c2:54:96:f0:00:01',
                u'maximumMbps': 10000,
                u'portId': u'Flb 1:1-b',
                u'name': 'connection1',
                u'functionType': 'FibreChannel',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': u'10:00:c2:54:96:f0:00:00',
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': None
            },
            {
                u'requestedMbps': 2500,
                u'deploymentStatus': u'Reserved',
                u'networkUri': u'/rest/fc-networks/617a2c3b-1505-4369-a0a5-4c169183bf9d',
                u'mac': u'46:E0:32:50:00:01',
                u'wwpnType': u'Virtual',
                u'id': 2,
                u'macType': u'Virtual',
                u'allocatedMbps': 0,
                u'wwnn': u'10:00:c2:54:96:f0:00:03',
                u'maximumMbps': 0,
                u'portId': 'None',
                u'name': 'connection2',
                u'functionType': 'FibreChannel',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': u'10:00:c2:54:96:f0:00:02',
                u'interconnectUri': None,
                u'requestedVFs': None
            }
        ]
        }

        self.assertTrue(resource_compare(resource1, resource2))

    def test_comparison_list_when_dict_has_diff_key(self):
        dict1 = {
            "name": "name",
            "value": [{'name': 'value1'},
                      {'name': 'value2'},
                      {'name': 3}]
        }

        dict2 = {
            "name": "name",
            "value": [{'count': 3},
                      {'name': 'value1'},
                      {'name': 'value2'}]
        }
        self.assertFalse(resource_compare(dict1, dict2))


if __name__ == '__main__':
    unittest.main()
