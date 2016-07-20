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
from hpOneView.resources.networking.network_sets import NetworkSets
from hpOneView.resources.resource import ResourceClient


class NetworkSetsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._network_sets = NetworkSets(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._network_sets.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test Network Set',
            'type': 'network-sets',
            'connectionTemplateUri': None,
            'nativeNetworkUri': None
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._network_sets.create(resource, 10)
        mock_create.assert_called_once_with(resource_rest_call, timeout=10)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_default_values(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test Network Set',
        }
        resource_with_default_values = {
            'name': 'OneViewSDK Test Network Set',
            'connectionTemplateUri': None,
            'type': 'network-set'
        }
        mock_create.return_value = {}

        self._network_sets.create(resource)

        mock_create.assert_called_once_with(resource_with_default_values, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test Network Set',
            'type': 'network-set',
            'uri': 'a_uri',
            'connectionTemplateUri': None
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._network_sets.update(resource, 20)
        mock_update.assert_called_once_with(resource_rest_call, timeout=20)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_default_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test Network Set',
        }
        resource_with_default_values = {
            'name': 'OneViewSDK Test Network Set',
            'connectionTemplateUri': None,
            'type': 'network-set',
        }
        mock_update.return_value = {}

        self._network_sets.update(resource)

        mock_update.assert_called_once_with(
            resource_with_default_values, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._network_sets.delete(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._network_sets.get_by('name', 'OneViewSDK Test Network Set')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK Test Network Set')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._network_sets.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/network-sets/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._network_sets.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_without_ethernet_called_once(self, mock_get):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri = '/rest/network-sets/ad28cf21-8b15-4f92-bdcf-51cb2042db32/withoutEthernet'
        self._network_sets.get_without_ethernet(id)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_without_ethernet_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._network_sets.get_all_without_ethernet(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)
