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
from hpOneView.resources.servers.server_profile_templates import ServerProfileTemplate
from hpOneView.resources.resource import Resource, ResourceHelper

TIMEOUT = -1


class ServerProfileTemplateTest(TestCase):

    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ServerProfileTemplate(http_connection)
        self.uri = "/rest/server-profile-templates/test"
        self._resource.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'
        self._resource.get_all(
            start=2, count=500, filter=query_filter, sort=sort, scope_uris=scope_uris)
        mock_get_all.assert_called_once_with(
            start=2, count=500, filter=query_filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create(self, mock_create):
        template = dict(name="BL460c Gen8 1")

        self._resource.create(template, timeout=TIMEOUT)
        mock_create.assert_called_once_with(
            template, None, -1, force=True
        )

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update(self, mock_update, mock_ensure_client):
        template = dict(name="BL460c Gen8 1", macType="Virtual")

        self._resource.update(template)
        template["uri"] = self.uri

        mock_update.assert_called_once_with(template, self.uri, True, -1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete(self, mock_delete):
        self._resource.delete(timeout=TIMEOUT)
        mock_delete.assert_called_once_with(self.uri, timeout=TIMEOUT, custom_headers=None, force=False)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_new_profile(self, mock_get):
        expected_uri = '{}/new-profile'.format(self.uri)

        self._resource.get_new_profile()
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_transformation(self, mock_get):
        enclosure_group_uri = "/rest/enclosure-groups/bb1fbca0-2289-4b75-adbb-0564cdc4995d"
        server_hardware_type_uri = "/rest/server-hardware-types/34A3A0B2-66C7-4657-995E-60895C1F8F96"

        transformation_path = self._resource.TRANSFORMATION_PATH.format(**locals())
        expected_uri = self.uri + transformation_path

        self._resource.get_transformation(enclosure_group_uri=enclosure_group_uri,
                                          server_hardware_type_uri=server_hardware_type_uri)

        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_available_networks(self, mock_get):
        uri = '/rest/server-profile-templates/available-networks?profileTemplateUri={}'.format(self.uri)

        self._resource.get_available_networks(profileTemplateUri=self.uri)
        mock_get.assert_called_once_with(uri)
