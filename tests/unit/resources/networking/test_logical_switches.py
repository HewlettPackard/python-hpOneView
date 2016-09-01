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
from hpOneView.resources.networking.logical_switches import LogicalSwitches
from hpOneView.resources.resource import ResourceClient


class LogicalSwitchesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._logical_switches = LogicalSwitches(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._logical_switches.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            "logicalSwitch": {
                "name": "Test Logical Switch",
                "state": "Active",
                "logicalSwitchGroupUri": "/rest/logical-switch-groups/e7401307-58bd-49ad-8a1b-79f351a346b8",
                "type": "set_by_user"
            },
            "switchCredentialConfiguration": [],
            "logicalSwitchCredentials": []
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._logical_switches.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_default_values(self, mock_create):
        resource = {
            "logicalSwitch": {
                "name": "Test Logical Switch"
            }
        }
        resource_with_default_values = {
            "logicalSwitch": {
                "name": "Test Logical Switch",
                "type": "logical-switch"
            }
        }
        mock_create.return_value = {}

        self._logical_switches.create(resource)

        mock_create.assert_called_once_with(resource_with_default_values, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        uri = '/rest/logical-switches/c4ae6a56-a595-4b06-8c7a-405212df8b93'
        resource = {
            "logicalSwitch": {
                "name": "Test Logical Switch",
                "state": "Active",
                "logicalSwitchGroupUri": "/rest/logical-switch-groups/7cc34511-0b00-4a48-82f6-1e9a662afeb8",
                "type": "set_by_user",
                "uri": uri
            },
            "switchCredentialConfiguration": [],
            "logicalSwitchCredentials": []
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._logical_switches.update(resource, 60)

        mock_update.assert_called_once_with(resource_rest_call, uri=uri, timeout=60)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_default_values(self, mock_update):
        uri = '/rest/logical-switches/c4ae6a56-a595-4b06-8c7a-405212df8b93'
        resource = {
            "logicalSwitch": {
                "name": "Test Logical Switch",
                "uri": uri
            },
            "uri": "a_uri"
        }
        resource_with_default_values = {
            "logicalSwitch": {
                "name": "Test Logical Switch",
                "type": "logical-switch",
                "uri": uri
            },
            "uri": "a_uri"
        }
        mock_update.return_value = {}

        self._logical_switches.update(resource)

        mock_update.assert_called_once_with(resource_with_default_values, uri=uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._logical_switches.delete(id, force=False, timeout=-1)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._logical_switches.get_by('name', 'Test Logical Switch')

        mock_get_by.assert_called_once_with('name', 'Test Logical Switch')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._logical_switches.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        uri = '/rest/logical-switches/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._logical_switches.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_refresh_by_uri(self, mock_update_with_zero_body):
        uri = '/rest/logical-switches/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-switches/ad28cf21-8b15-4f92-bdcf-51cb2042db32/refresh'

        self._logical_switches.refresh(uri)

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_refresh_by_id(self, mock_update_with_zero_body):
        mock_update_with_zero_body.return_value = {}
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-switches/ad28cf21-8b15-4f92-bdcf-51cb2042db32/refresh'

        self._logical_switches.refresh(id)

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)
