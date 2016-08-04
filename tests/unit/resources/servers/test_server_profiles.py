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
from hpOneView.resources.servers.server_profiles import ServerProfiles

TIMEOUT = -1


class ServerProfilesTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ServerProfiles(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = 'name=TestName'
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, filter=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=query_filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"

        self._resource.get(id)
        mock_get.assert_called_once_with(id_or_uri=id)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_property(self, mock_get_by):
        profile_property = "name"
        profile_name = "Server Profile Test"

        self._resource.get_by(profile_property, profile_name)
        mock_get_by.assert_called_once_with(profile_property, profile_name)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name(self, mock_get_by_name):
        profile_name = "Server Profile Test"

        self._resource.get_by_name(profile_name)
        mock_get_by_name.assert_called_once_with(profile_name)

    @mock.patch.object(ResourceClient, 'create')
    def test_create(self, mock_create):
        template = dict(name="Server Profile Test")

        expected_template = template.copy()
        expected_template["type"] = "ServerProfileV5"

        self._resource.create(resource=template, timeout=TIMEOUT)
        mock_create.assert_called_once_with(resource=expected_template, timeout=TIMEOUT)

    @mock.patch.object(ResourceClient, 'update')
    def test_update(self, mock_update):
        uri = "/rest/server-profiles/4ff2327f-7638-4b66-ad9d-283d4940a4ae"
        template = dict(name="Server Profile Test", macType="Virtual")

        expected_template = template.copy()
        expected_template["type"] = "ServerProfileV5"

        self._resource.update(resource=template, id_or_uri=uri)
        mock_update.assert_called_once_with(resource=expected_template, uri=uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete(self, mock_delete):
        template = dict(name="Server Profile Test")

        self._resource.delete(resource=template, timeout=TIMEOUT)
        mock_delete.assert_called_once_with(resource=template, timeout=TIMEOUT)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch(self, mock_pacth):
        uri = "/rest/server-profiles/4ff2327f-7638-4b66-ad9d-283d4940a4ae"

        self._resource.patch(uri, "replace", "/templateCompliance", "Compliant")
        mock_pacth.assert_called_once_with(uri, "replace", "/templateCompliance", "Compliant", -1)

    @mock.patch.object(ResourceClient, 'get_schema')
    def test_get_schema(self, get_schema):
        self._resource.get_schema()
        get_schema.assert_called_once()

    @mock.patch.object(ResourceClient, 'get')
    def test_get_compliance_preview(self, mock_get):
        server_uri = "/rest/server-profiles/4ff2327f-7638-4b66-ad9d-283d4940a4ae"
        uri = "/rest/server-profiles/4ff2327f-7638-4b66-ad9d-283d4940a4ae/compliance-preview"

        self._resource.get_compliance_preview(server_uri)
        mock_get.assert_called_once_with(uri)
