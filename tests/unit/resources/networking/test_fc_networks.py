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
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.resource import Resource, ResourcePatchMixin


class FcNetworksTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fc_networks = FcNetworks(self.connection)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fc_networks.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter, sort)

    @mock.patch.object(Resource, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': True,
            'type': 'fc-networkV2',
            'linkStabilityTime': 20,
            'fabricType': None,
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._fc_networks.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, 30)

    @mock.patch.object(Resource, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 20,
            'fabricType': None,
            'uri': 'a_uri',
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._fc_networks.update(resource, 60)
        mock_update.assert_called_once_with(resource_rest_call, 60)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._fc_networks.delete(force=False, timeout=-1)
        mock_delete.assert_called_once_with(force=False, timeout=-1)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fc_networks.get_by('name', 'OneViewSDK "Test FC Network')
        mock_get_by.assert_called_once_with('name', 'OneViewSDK "Test FC Network')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/fc-networks/3518be0e-17c1-4189-8f81-83f3724f6155'

        self._fc_networks.get_by_uri(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._fc_networks.patch('/rest/fake/fc123', 'replace', '/scopeUris', ['/rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('/rest/fake/fc123', 'replace', '/scopeUris',
                                           ['/rest/fake/scope123'], 1)
