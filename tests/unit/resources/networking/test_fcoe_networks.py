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
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class FcoeNetworksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fcoe_networks = FcoeNetworks(self.connection)
        self.uri = "/rest/fcoe-networks/3518be0e-17c1-4189-8f81-83f3724f6155"
        self._fcoe_networks.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fcoe_networks.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test FCoE Network',
        }

        mock_create.return_value = {}

        self._fcoe_networks.create(resource)

        mock_create.assert_called_once_with(resource, None, -1, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update(self, mock_update, mock_ensure_client):
        resource = {
            'name': 'vsan1',
            'vlanId': '201',
            'connectionTemplateUri': None,
            'type': 'fcoe-networkV2',
        }
        resource_rest_call = resource.copy()
        resource_rest_call.update(self._fcoe_networks.data)
        mock_update.return_value = {}

        self._fcoe_networks.update(resource, timeout=12)
        mock_update.assert_called_once_with(resource_rest_call, self.uri, False, 12, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._fcoe_networks.delete(force=False, timeout=50)

        mock_delete.assert_called_once_with(self.uri, force=False,
                                            custom_headers=None, timeout=50)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fcoe_networks.get_by('name', 'OneViewSDK Test FCoE Network')

        mock_get_by.assert_called_once_with('name', 'OneViewSDK Test FCoE Network')

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch_request):
        mock_patch_request.return_value = {}

        self._fcoe_networks.patch('replace', '/scopeUris', ['/rest/fake/scope123'], timeout=-1)
        mock_patch_request.assert_called_once_with(self.uri,
                                                   body=[{'path': '/scopeUris',
                                                          'value': ['/rest/fake/scope123'],
                                                          'op': 'replace'}],
                                                   custom_headers=None,
                                                   timeout=-1)
