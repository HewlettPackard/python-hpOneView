# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.resource import ResourceClient


class UplinkSetsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._uplink_sets = UplinkSets(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self._uplink_sets.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_defaults(self, mock_get_all):
        self._uplink_sets.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._uplink_sets.get_by('name', 'OneViewSDK Test Uplink Set')

        mock_get_by.assert_called_once_with('name', 'OneViewSDK Test Uplink Set')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._uplink_sets.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/uplink-sets/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._uplink_sets.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            "type": "uplink-setV2",
            "name": "uls2",
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._uplink_sets.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_default_values(self, mock_create):
        resource = {
            "name": "uls2",
        }
        resource_with_default_values = {
            "type": "uplink-setV3",
            "name": "uls2",
        }
        mock_create.return_value = {}

        self._uplink_sets.create(resource)
        mock_create.assert_called_once_with(resource_with_default_values, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            "type": "uplink-setV2",
            "name": "uls2",
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._uplink_sets.update(resource, 60)
        mock_update.assert_called_once_with(resource_rest_call, timeout=60)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_default_values(self, mock_update):
        resource = {
            "name": "uls2",
        }
        resource_with_default_values = {
            "type": "uplink-setV3",
            "name": "uls2",
        }
        mock_update.return_value = {}

        self._uplink_sets.update(resource)
        mock_update.assert_called_once_with(resource_with_default_values, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._uplink_sets.delete(id, force=False, timeout=-1)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(EthernetNetworks, 'get')
    @mock.patch.object(UplinkSets, 'get')
    def test_get_ethernet_networks(self, mock_uplink_get, mock_get_enet):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
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

        mock_uplink_get.return_value = uplink
        mock_get_enet.side_effect = result_get_enet
        result = self._uplink_sets.get_ethernet_networks(id)
        self.assertEqual(mock_get_enet.call_count, 3)
        self.assertEqual(result_get_enet, result)

    @mock.patch.object(EthernetNetworks, 'get')
    @mock.patch.object(UplinkSets, 'get')
    def test_get_ethernet_networks_with_empty_list(self, mock_uplink_get, mock_get_enet):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uplink = {
            'name': 'UplinkName',
        }

        mock_uplink_get.return_value = uplink
        result = self._uplink_sets.get_ethernet_networks(id)
        self.assertEqual([], result)
