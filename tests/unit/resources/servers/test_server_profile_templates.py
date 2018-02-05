# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.resource import ResourceClient

TIMEOUT = -1


class ServerProfileTemplateTest(TestCase):

    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ServerProfileTemplate(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'
        self._resource.get_all(
            start=2, count=500, filter=query_filter, sort=sort, scope_uris=scope_uris)
        mock_get_all.assert_called_once_with(
            start=2, count=500, filter=query_filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        template_id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"

        self._resource.get(template_id)
        mock_get.assert_called_once_with(id_or_uri=template_id)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_property(self, mock_get_by):
        template_property = "name"
        template_name = "BL460c Gen8 1"

        self._resource.get_by(template_property, template_name)
        mock_get_by.assert_called_once_with(template_property, template_name)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name(self, mock_get_by_name):
        template_name = "BL460c Gen8 1"

        self._resource.get_by_name(template_name)
        mock_get_by_name.assert_called_once_with(template_name)

    @mock.patch.object(ResourceClient, 'create')
    def test_create(self, mock_create):
        uri = "/rest/server-profile-templates?force=True"
        template = dict(name="BL460c Gen8 1")

        self._resource.create(resource=template, timeout=TIMEOUT)
        mock_create.assert_called_once_with(
            resource=template,
            uri=uri,
            timeout=TIMEOUT,
            default_values=ServerProfileTemplate.DEFAULT_VALUES
        )

    @mock.patch.object(ResourceClient, 'update')
    def test_update(self, mock_update):
        uri = "/rest/server-profile-templates/4ff2327f-7638-4b66-ad9d-283d4940a4ae"
        template = dict(name="BL460c Gen8 1", macType="Virtual")

        self._resource.update(resource=template, id_or_uri=uri)
        mock_update.assert_called_once_with(
            resource=template,
            uri=uri,
            default_values=ServerProfileTemplate.DEFAULT_VALUES,
            force=True
        )

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete(self, mock_delete):
        template = dict(name="BL460c Gen8 1")

        self._resource.delete(resource=template, timeout=TIMEOUT)
        mock_delete.assert_called_once_with(resource=template, timeout=TIMEOUT, force=True)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_new_profile(self, mock_get):
        template_id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"
        expected_uri = '/rest/server-profile-templates/6fee02f3-b7c7-42bd-a528-04341e16bad6/new-profile'

        self._resource.get_new_profile(id_or_uri=template_id)
        mock_get.assert_called_once_with(id_or_uri=expected_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_transformation(self, mock_get):
        template_id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"
        enclosure_group_uri = "/rest/enclosure-groups/bb1fbca0-2289-4b75-adbb-0564cdc4995d"
        server_hardware_type_uri = "/rest/server-hardware-types/34A3A0B2-66C7-4657-995E-60895C1F8F96"

        transformation_path = self._resource.TRANSFORMATION_PATH.format(**locals())
        template_uri = '/rest/server-profile-templates/6fee02f3-b7c7-42bd-a528-04341e16bad6'
        expected_uri = template_uri + transformation_path

        self._resource.get_transformation(id_or_uri=template_id,
                                          enclosure_group_uri=enclosure_group_uri,
                                          server_hardware_type_uri=server_hardware_type_uri)

        mock_get.assert_called_once_with(id_or_uri=expected_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_available_networks(self, mock_get):
        template_uri = "/rest/server-profile-templates/6fee02f3-b7c7-42bd-a528-04341e16bad6"
        uri = '/rest/server-profile-templates/available-networks?profileTemplateUri={}'.format(template_uri)

        self._resource.get_available_networks(profileTemplateUri=template_uri)
        mock_get.assert_called_once_with(id_or_uri=uri)
