# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.ethernet_networks import EthernetNetworks
from hpOneView.resources.resource import Resource, ResourcePatchMixin, ResourceHelper


class EthernetNetworksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._ethernet_networks = EthernetNetworks(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._ethernet_networks.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, filter=filter, sort=sort, start=2)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'vlanId': 10,
            'name': 'OneViewSDK Test Ethernet Network',
            "ethernetNetworkType": "Tagged",
            "purpose": "Management",
            "connectionTemplateUri": None,
            "smartLink": False,
            "privateNetwork": False
        }
        resource_rest_call = resource.copy()
        resource_rest_call['type'] = 'ethernet-networkV300'
        mock_create.return_value = {}

        self._ethernet_networks.create(resource, timeout=12)
        mock_create.assert_called_once_with(resource_rest_call, None, 12, None, False)

    @mock.patch.object(ResourceHelper, 'create')
    @mock.patch.object(Resource, 'get_all')
    def test_create_bulk(self, mock_get_all, mock_create):
        resource = {
            'vlanIdRange': '1-10',
            'purpose': 'General',
            'namePrefix': 'TestNetwork',
            'smartLink': False,
            'privateNetwork': False,
            'bandwidth': {
                'maximumBandwidth': 10000,
                'typicalBandwidth': 2000
            }
        }
        resource_rest_call = resource.copy()
        resource_rest_call['type'] = 'bulk-ethernet-network'

        mock_create.return_value = {}
        mock_get_all.return_value = []

        self._ethernet_networks.create_bulk(resource, 27)

        mock_create.assert_called_once_with(
            resource_rest_call, uri='/rest/ethernet-networks/bulk', timeout=27)
        mock_get_all.assert_called_once_with(
            filter='"\'name\' matches \'TestNetwork\\_%\'"', sort='vlanId:ascending')

    @mock.patch.object(Resource, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test Ethernet Network',
            'smartLink': False,
            'connectionTemplateUri': None,
            'vlanId': None,
            'privateNetwork': True,
            'ethernetNetworkType': 'Untagged',
            'purpose': 'General'
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._ethernet_networks.update(resource, timeout=60)
        mock_update.assert_called_once_with(resource_rest_call, timeout=60)

    @mock.patch.object(Resource, 'update')
    def test_update_should_use_default_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test Ethernet Network',
        }

        mock_update.return_value = {}

        self._ethernet_networks.update(resource)

        mock_update.assert_called_once_with(resource)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._ethernet_networks.delete(id, force=False, timeout=-1)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._ethernet_networks.get_by(
            'name', 'OneViewSDK Test Ethernet Network')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK Test Ethernet Network')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_associated_uplink_groups_uri_called_once_with_uri(self, mock_get):
        self._ethernet_networks.data = {"name": "name",
                                        "uri": "/rest/ethernet-networks/3518be0e-17c1-4189-8f81-83f3724f6155"}
        self._ethernet_networks.get_associated_uplink_groups()

        uri = '/rest/ethernet-networks/3518be0e-17c1-4189-8f81-83f3724f6155/associatedUplinkGroups'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_associated_profiles_called_once_with_uri(self, mock_get):
        self._ethernet_networks.data = {"name": "name",
                                        "uri": "/rest/ethernet-networks/3518be0e-17c1-4189-8f81-83f3724f6155"}
        self._ethernet_networks.get_associated_profiles()

        uri = '/rest/ethernet-networks/3518be0e-17c1-4189-8f81-83f3724f6155/associatedProfiles'

        mock_get.assert_called_once_with(uri)

    def __mock_enet_gel_all(self):
        return [
            {'name': 'TestNetwork_1', 'vlanId': 1},
            {'name': 'TestNetwork_2', 'vlanId': 2},
            {'name': 'TestNetwork_3', 'vlanId': 3},
            {'name': 'TestNetwork_4', 'vlanId': 4},
            {'name': 'TestNetwork_5', 'vlanId': 5},
            {'name': 'TestNetwork_5', 'vlanId': 6},
            {'name': 'TestNetwork_7', 'vlanId': 7},
            {'name': 'TestNetwork_8', 'vlanId': 8},
            {'name': 'TestNetwork_9', 'vlanId': 9},
            {'name': 'TestNetwork_10', 'vlanId': 10},
        ]

    @mock.patch.object(EthernetNetworks, 'get_all')
    def test_get_bulk_with_one_range(self, mock_get_all):
        mock_get_all.return_value = self.__mock_enet_gel_all()

        expected_result = [
            {'name': 'TestNetwork_1', 'vlanId': 1},
            {'name': 'TestNetwork_2', 'vlanId': 2},
            {'name': 'TestNetwork_3', 'vlanId': 3},
            {'name': 'TestNetwork_4', 'vlanId': 4},
        ]

        result = self._ethernet_networks.get_range('TestNetwork', '1-4')
        self.assertEqual(result, expected_result)

    @mock.patch.object(EthernetNetworks, 'get_all')
    def test_get_bulk_with_one_value(self, mock_get_all):
        mock_get_all.return_value = self.__mock_enet_gel_all()

        expected_result = [
            {'name': 'TestNetwork_1', 'vlanId': 1},
            {'name': 'TestNetwork_2', 'vlanId': 2},
        ]

        result = self._ethernet_networks.get_range('TestNetwork', '2')
        self.assertEqual(result, expected_result)

    @mock.patch.object(EthernetNetworks, 'get_all')
    def test_get_bulk_with_one_value_and_one_range(self, mock_get_all):
        mock_get_all.return_value = self.__mock_enet_gel_all()

        expected_result = [
            {'name': 'TestNetwork_2', 'vlanId': 2},
            {'name': 'TestNetwork_9', 'vlanId': 9},
            {'name': 'TestNetwork_10', 'vlanId': 10},
        ]

        result = self._ethernet_networks.get_range('TestNetwork', '2, 9-10')
        self.assertEqual(result, expected_result)

    @mock.patch.object(EthernetNetworks, 'get_all')
    def test_get_bulk_with_multiple_values(self, mock_get_all):
        mock_get_all.return_value = self.__mock_enet_gel_all()

        expected_result = [
            {'name': 'TestNetwork_9', 'vlanId': 9},
            {'name': 'TestNetwork_10', 'vlanId': 10},
        ]

        result = self._ethernet_networks.get_range('TestNetwork', '9,10')
        self.assertEqual(result, expected_result)

    @mock.patch.object(EthernetNetworks, 'get_all')
    def test_get_bulk_with_multiple_ranges(self, mock_get_all):
        mock_get_all.return_value = self.__mock_enet_gel_all()

        expected_result = [
            {'name': 'TestNetwork_5', 'vlanId': 6},
            {'name': 'TestNetwork_7', 'vlanId': 7},
            {'name': 'TestNetwork_9', 'vlanId': 9},
            {'name': 'TestNetwork_10', 'vlanId': 10},
        ]

        result = self._ethernet_networks.get_range('TestNetwork', '6-7,9-10')
        self.assertEqual(result, expected_result)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    @mock.patch.object(Resource, 'get_by')
    def test_patch_should_use_user_defined_values(self, mock_get_by, mock_patch):
        mock_patch.return_value = {}
        self._ethernet_networks.data = {"name": "test name", "uri": "/rest/test"}
        self._ethernet_networks.patch('replace', '/scopeUris', ['/rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('/rest/test',
                                           body=[{u'path': '/scopeUris', u'value': ['/rest/fake/scope123'], u'op': 'replace'}],
                                           custom_headers=1, timeout=-1)

    def test_dissociate_values_or_ranges_with_one_value(self):
        expected_result = [1, 2, 3, 4, 5]
        result = self._ethernet_networks.dissociate_values_or_ranges('5')
        self.assertEqual(result, expected_result)

    def test_dissociate_values_or_ranges_with_multiple_values(self):
        expected_result = [6, 7, 9]
        result = self._ethernet_networks.dissociate_values_or_ranges('6,7,9')
        self.assertEqual(result, expected_result)

    def test_dissociate_values_or_ranges_with_one_range(self):
        expected_result = [6, 7]
        result = self._ethernet_networks.dissociate_values_or_ranges('6-7')
        self.assertEqual(result, expected_result)

    def test_dissociate_values_or_ranges_with_multiple_ranges(self):
        expected_result = [6, 7, 9, 10]
        result = self._ethernet_networks.dissociate_values_or_ranges('6-7,9-10')
        self.assertEqual(result, expected_result)
