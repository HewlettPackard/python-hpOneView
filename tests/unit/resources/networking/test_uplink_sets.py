# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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

import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.ethernet_networks import EthernetNetworks
from hpOneView.resources.networking.uplink_sets import UplinkSets
from hpOneView.resources.resource import Resource, ResourceHelper


class UplinkSetsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._uplink_sets = UplinkSets(self.connection)
        self._uplink_sets.data = {'uri': '/rest/ul-inksets/ad28cf21-8b15-4f92-bdcf-51cb2042db32'}
        self._ethernet_networks = EthernetNetworks(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self._uplink_sets.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_defaults(self, mock_get_all):
        self._uplink_sets.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter='', sort='', start=0)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._uplink_sets.get_by('name', 'OneViewSDK Test Uplink Set')

        mock_get_by.assert_called_once_with('name', 'OneViewSDK Test Uplink Set')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/uplink-sets/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._uplink_sets.get_by_uri(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_should_be_called_once(self, mock_create):
        resource = {
            "type": "uplink-setV3",
            "name": "uls2",
        }
        mock_create.return_value = {}

        self._uplink_sets.create(resource, 60)
        mock_create.assert_called_once_with(resource, 60, -1, None, False)

    @mock.patch.object(Resource, 'update')
    def test_update_should_be_called_once(self, mock_update):
        resource = {
            "name": "uls2",
        }
        mock_update.return_value = {}

        self._uplink_sets.update(resource)
        mock_update.assert_called_once_with(resource)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._uplink_sets.delete(force=False, timeout=-1)

        mock_delete.assert_called_once_with(force=False, timeout=-1)

    @mock.patch.object(EthernetNetworks, 'get_by_uri')
    def test_get_ethernet_networks(self, mock_get_enet):
        uplink = {
            'name': 'UplinkName',
            'networkUris': ['/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939',
                            '/rest/ethernet-networks/d34dcf5e-0d8e-441c-b00d-e1dd6a067188',
                            '/rest/ethernet-networks/fg0dcf5e-1589-4mn0-852f-85hd6a067963',
                            ],
        }

        result_get_enet = [
            {'name': 'Ethernet Network 1'},
            {'name': 'Ethernet Network 2'},
            {'name': 'Ethernet Network 3'},
        ]

        self._uplink_sets.data = uplink
        mock_get_enet.side_effect = result_get_enet
        result = self._uplink_sets.get_ethernet_networks()

        self.assertEqual(mock_get_enet.call_count, 3)
        self.assertEqual(result_get_enet, result)

    @mock.patch.object(UplinkSets, 'get_by_uri')
    def test_get_ethernet_networks_with_empty_list(self, mock_uplink_get):
        uplink = {
            'name': 'UplinkName',
        }

        mock_uplink_get.return_value = None
        self._uplink_sets.data = uplink
        result = self._uplink_sets.get_ethernet_networks()
        self.assertEqual([], result)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_add_one_ethernet_network(self, mock_ethnet_get, mock_uplink_update):
        ethernet_to_add = 'eth1'
        uplink = {
            'name': 'UplinkName',
        }

        uplink_to_update = {
            'networkUris': ['/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939', ]
        }

        self._ethernet_networks.data = {'uri': '/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939'}
        mock_ethnet_get.return_value = self._ethernet_networks

        self._uplink_sets.data = uplink
        self._uplink_sets.add_ethernet_networks(ethernet_to_add)
        mock_uplink_update.assert_called_once_with(uplink_to_update)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_add_a_list_of_ethernet_networks(self, mock_ethnet_get, mock_uplink_update):
        ethernet_to_add = [
            'eth1',
            'eth2',
        ]

        uplink_to_update = {
            'networkUris': ['/rest/ethernet-networks/134dcf5e-0d8e-441c-b00d-e1dd6a067188',
                            '/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939', ]
        }

        eth1 = self._ethernet_networks
        eth2 = EthernetNetworks(self.connection)
        eth1.data = {'name': 'eth1', 'uri': '/rest/ethernet-networks/134dcf5e-0d8e-441c-b00d-e1dd6a067188'}
        eth2.data = {'name': 'eth2', 'uri': '/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939'}
        result_get_enet = [eth1, eth2]

        mock_ethnet_get.side_effect = result_get_enet

        self._uplink_sets.add_ethernet_networks(ethernet_to_add)
        mock_uplink_update.assert_called_once_with(uplink_to_update)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_add_missing_ethernet_networks(self, mock_ethnet_get, mock_uplink_update):
        ethernet_to_add = [
            'eth1',
            'eth2',
        ]
        uplink = {
            'name': 'UplinkName',
            'networkUris': ['/rest/ethernet-networks/d34dcf5e-0d8e-441c-b00d-e1dd6a067188', ]
        }
        uplink_to_update = {
            'networkUris': ['/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939',
                            '/rest/ethernet-networks/d34dcf5e-0d8e-441c-b00d-e1dd6a067188', ]
        }

        eth1 = self._ethernet_networks
        eth2 = EthernetNetworks(self.connection)
        eth1.data = {'name': 'eth1', 'uri': '/rest/ethernet-networks/d34dcf5e-0d8e-441c-b00d-e1dd6a067188'}
        eth2.data = {'name': 'eth2', 'uri': '/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939'}
        result_get_enet = [eth1, eth2]

        self._uplink_sets.data = uplink
        mock_ethnet_get.side_effect = result_get_enet

        self._uplink_sets.add_ethernet_networks(ethernet_to_add)
        mock_uplink_update.assert_called_once_with(uplink_to_update)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_not_add_ethernet_networks_already_associated(self, mock_uplink_get, mock_uplink_update):
        ethernet_to_add = [
            'eth1',
        ]

        uplink = {
            'name': 'UplinkName',
            'networkUris': ['/rest/ethernet-networks/d34dcf5e-0d8e-441c-b00d-e1dd6a067188', ]
        }

        self._ethernet_networks.data = {'uri': '/rest/ethernet-networks/d34dcf5e-0d8e-441c-b00d-e1dd6a067188'}
        mock_uplink_get.return_value = self._ethernet_networks

        self._uplink_sets.data = uplink
        result = self._uplink_sets.add_ethernet_networks(ethernet_to_add)
        self.assertEqual(mock_uplink_update.call_count, 0)
        self.assertEqual(uplink, result)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_remove_one_ethernet_network(self, mock_ethernet_get, mock_uplink_update):
        ethernet_to_remove = 'eth1'
        uplink = {
            'name': 'UplinkName',
            'networkUris': ['/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939', ]
        }

        uplink_to_update = {
            'networkUris': []
        }

        self._ethernet_networks.data = {'uri': '/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939'}
        mock_ethernet_get.return_value = self._ethernet_networks

        self._uplink_sets.data = uplink
        self._uplink_sets.remove_ethernet_networks(ethernet_to_remove)
        mock_uplink_update.assert_called_once_with(uplink_to_update)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_remove_a_list_of_ethernet_networks(self, mock_ethernet_get, mock_uplink_update):
        ethernet_to_remove = ['eth1']

        uplink = {
            'name': 'UplinkName',
            'networkUris': ['/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939',
                            '/rest/ethernet-networks/45gdo84i-6jgf-093b-gsd5-njkn543tb64l']
        }

        uplink_to_update = {
            'networkUris': ['/rest/ethernet-networks/45gdo84i-6jgf-093b-gsd5-njkn543tb64l', ]
        }

        self._ethernet_networks.data = {'name': 'eth1',
                                        'uri': '/rest/ethernet-networks/5f14bf27-f839-4e9f-9ec8-9f0e0b413939'}
        mock_ethernet_get.return_value = self._ethernet_networks

        self._uplink_sets.data = uplink
        self._uplink_sets.remove_ethernet_networks(ethernet_to_remove)
        mock_uplink_update.assert_called_once_with(uplink_to_update)

    @mock.patch.object(UplinkSets, 'update')
    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_not_remove_ethernet_networks_already_not_associated(self, mock_uplink_get, mock_uplink_update):
        ethernet_to_remove = [
            'eth1',
        ]
        uplink = {
            'name': 'UplinkName',
            'networkUris': ['/rest/ethernet-networks/45gdo84i-6jgf-093b-gsd5-njkn543tb64l', ]
        }

        self._ethernet_networks.data = {'name': 'eth1',
                                        'uri': '/rest/ethernet-networks/45gdo84i-6jgf-093b-gsd5-njk33'}
        mock_uplink_get.return_value = self._ethernet_networks

        self._uplink_sets.data = uplink
        result = self._uplink_sets.remove_ethernet_networks(ethernet_to_remove)

        self.assertEqual(mock_uplink_update.call_count, 0)
        self.assertEqual(uplink, result)

    @mock.patch.object(EthernetNetworks, 'get_by_name')
    def test_set_ethernet_uris_with_invalid_operation(self, mock_uplink_get):
        ethernet_to_add = [
            'eth1',
        ]

        # Force a private call with invalid operation (aims to reach 100% coverage)
        self.assertRaises(ValueError,
                          self._uplink_sets._UplinkSets__set_ethernet_uris,
                          ethernet_to_add, "invalid_operation")

        mock_uplink_get.assert_called_once_with(ethernet_to_add[0])
