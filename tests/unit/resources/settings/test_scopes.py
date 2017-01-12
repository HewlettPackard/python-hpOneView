# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.settings.scopes import Scopes


class ScopesTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        oneview_connection = connection(self.DEFAULT_HOST)
        self.resource = Scopes(oneview_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        sort = 'name:ascending'
        query = 'name eq "TestName"'
        view = 'expand'

        self.resource.get_all(2, 500, sort, query, view)
        mock_get_all.assert_called_once_with(2, 500, sort=sort, query=query, view=view)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_scope_when_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SampleScope1", "uri": "/rest/scopes/1"},
            {"name": "SampleScope2", "uri": "/rest/scopes/2"}
        ]
        scope = self.resource.get_by_name("SampleScope2")
        expected_result = {"name": "SampleScope2", "uri": "/rest/scopes/2"}

        self.assertEqual(scope, expected_result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_null_when_not_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SampleScope1", "uri": "/rest/scopes/1"},
            {"name": "SampleScope2", "uri": "/rest/scopes/2"}
        ]
        scope = self.resource.get_by_name("SampleScope3")

        self.assertIsNone(scope)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self.resource.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/scopes/3518be0e-17c1-4189-8f81-83f3724f6155'
        self.resource.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        data = {
            'name': 'Name of the Scope'
        }
        data_rest_call = data.copy()

        self.resource.create(data, 30)
        mock_create.assert_called_once_with(data_rest_call, timeout=30,
                                            default_values=self.resource.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        data = {
            'name': 'Name of the Scope',
            'uri': 'a_uri'
        }
        data_rest_call = data.copy()

        self.resource.update(data, 60)

        headers = {'If-Match': '*'}
        mock_update.assert_called_once_with(data_rest_call, timeout=60,
                                            default_values=self.resource.DEFAULT_VALUES,
                                            custom_headers=headers)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_verify_if_match_etag_when_provided(self, mock_update):
        data = {'eTag': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}

        self.resource.update(data, -1)

        headers = {'If-Match': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}
        mock_update.assert_called_once_with(mock.ANY, timeout=mock.ANY, default_values=mock.ANY,
                                            custom_headers=headers)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self.resource.delete(id, timeout=-1)

        mock_delete.assert_called_once_with(id, timeout=-1, custom_headers={'If-Match': '*'})

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_should_verify_if_match_etag_when_provided(self, mock_delete):
        data = {'uri': 'a_uri',
                'eTag': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}

        self.resource.delete(data, -1)

        headers = {'If-Match': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}
        mock_delete.assert_called_once_with(mock.ANY, timeout=mock.ANY, custom_headers=headers)

    @mock.patch.object(ResourceClient, 'patch_request')
    def test_update_resource_assignments_called_once(self, mock_patch_request):
        uri = '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2'

        information = {
            "addedResourceUris": ["/rest/ethernet-networks/e801b73f-b4e8-4b32-b042-36f5bac2d60f"],
            "removedResourceUris": ["/rest/ethernet-networks/390bc9f9-cdd5-4c70-b38f-cf04e64f5c72"]
        }
        self.resource.update_resource_assignments(uri, information)

        mock_patch_request.assert_called_once_with(
            '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2/resource-assignments',
            information.copy(),
            custom_headers={'Content-Type': 'application/json'},
            timeout=-1)
